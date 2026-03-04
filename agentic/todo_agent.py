import json
from rich.console import Console
from .memory import TodoMemory
from .llm import LLMClient


class TodoAgent:

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self._memory = TodoMemory()
        self._llm = LLMClient(model=model)
        self._console = Console()
        self._tools = self._get_tools()

    def add_task(self, text: str) -> None:
        self._memory.add(text)
        self._console.print(f"[green]Added:[/green] {text}")

    def complete_task(self, index: int) -> None:
        self._memory.complete(index)
        self._console.print(f"[blue]Completed task {index+1}[/blue]")

    def show_tasks(self) -> None:
        report = self._memory.report()
        if report:
            self._console.print(report)
        else:
            self._console.print("No tasks.")

    def plan_tasks(self) -> None:
        todos = self._memory.report()

        prompt = f"""
You are a productivity assistant.

Here are the tasks:

{todos}

Suggest the best order to complete them and explain why.
"""

        plan = self._llm.generate(prompt)
        self._console.print("[bold]AI Plan[/bold]")
        self._console.print(plan)

    def _get_tools(self) -> list:
        """Get the function calling tools for OpenAI."""
        create_todos_json = {
            "name": "create_todos",
            "description": "Add new todos from a list of descriptions and return the full list",
            "parameters": {
                "type": "object",
                "properties": {
                    "descriptions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "title": "Descriptions"
                    }
                },
                "required": ["descriptions"],
                "additionalProperties": False
            }
        }

        mark_complete_json = {
            "name": "mark_complete",
            "description": "Mark complete the todo at the given position (starting from 1) and return the full list",
            "parameters": {
                "properties": {
                    "index": {
                        "description": "The 1-based index of the todo to mark as complete",
                        "title": "Index",
                        "type": "integer"
                    },
                    "completion_notes": {
                        "description": "Notes about how you completed the todo in rich console markup",
                        "title": "Completion Notes",
                        "type": "string"
                    }
                },
                "required": ["index", "completion_notes"],
                "type": "object",
                "additionalProperties": False
            }
        }

        return [
            {"type": "function", "function": create_todos_json},
            {"type": "function", "function": mark_complete_json}
        ]

    def _handle_tool_calls(self, tool_calls) -> list:
        """Handle tool calls from OpenAI and return tool results."""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            
            if tool_name == "create_todos":
                result = self._memory.create_todos(arguments["descriptions"])
            elif tool_name == "mark_complete":
                result = self._memory.mark_complete(
                    arguments["index"],
                    arguments["completion_notes"]
                )
                # Print completion notes if provided
                if arguments.get("completion_notes"):
                    self._console.print(arguments["completion_notes"])
            else:
                result = f"Unknown tool: {tool_name}"
            
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        
        return results

    def _validate_messages(self, messages: list) -> None:
        """Validate that messages are in the correct format."""
        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"messages[{i}] is not dict: {type(msg)} → {msg}")

            if "role" not in msg or "content" not in msg:
                raise ValueError(f"messages[{i}] missing role/content → {msg}")

            if not isinstance(msg["content"], str):
                raise ValueError(
                    f"messages[{i}].content not string: {type(msg['content'])} → {msg}"
                )

    def solve_problem(self, system_message: str, user_message: str, verbose: bool = False) -> str:
        """
        Solve a problem by creating a plan with todo tools, then executing it.
        Uses OpenAI function calling to allow the LLM to interact with todo tools.
        
        Args:
            system_message: System prompt instructing the agent how to behave
            user_message: The problem or task to solve
            verbose: If True, print message trace during execution
            
        Returns:
            The solution to the problem
        """
        # Clear any existing tasks
        self._memory._todos.clear()
        
        # Create initial messages
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        # Validate messages
        self._validate_messages(messages)
        
        # Loop until we get a final answer
        done = False
        while not done:
            if verbose:
                self._console.print("\n[dim]--- MESSAGE TRACE ---[/dim]")
                for i, m in enumerate(messages):
                    self._console.print(f"[dim]{i}: {m}[/dim]")
            
            # Get response from LLM
            response = self._llm.chat(messages, tools=self._tools)
            finish_reason = response["finish_reason"]
            message = response["message"]
            tool_calls = response["tool_calls"]
            
            if finish_reason == "tool_calls" and tool_calls:
                # Add assistant message with tool calls
                # Serialize tool_calls properly for the messages list
                tool_calls_serialized = [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in tool_calls
                ]
                
                messages.append({
                    "role": message.role,
                    "content": message.content or "",
                    "tool_calls": tool_calls_serialized
                })
                
                # Handle tool calls and add results
                results = self._handle_tool_calls(tool_calls)
                messages.extend(results)
                continue
            else:
                # We have a final answer
                done = True
                solution = message.content or ""
                self._console.print("[bold green]Solution:[/bold green]")
                self._console.print(solution)
                return solution