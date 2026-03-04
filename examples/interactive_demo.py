#!/usr/bin/env python3
"""
Interactive demo for the Todo Agent.
Ask questions and watch the agent solve them step by step using todo tools.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agentic.todo_agent import TodoAgent
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

# System message for the agent
SYSTEM_MESSAGE = """
You are given a problem to solve, by using your todo tools to plan a list of steps, then carrying out each step in turn.
Now use the todo list tools, create a plan, carry out the steps, and reply with the solution.
If any quantity isn't provided in the question, then include a step to come up with a reasonable estimate.
Provide your solution in Rich console markup without code blocks.
Do not ask the user questions or clarification; respond only with the answer after using your tools.
"""


def main():
    console.print(Panel.fit(
        "[bold cyan]🤖 Todo Agent Interactive Demo[/bold cyan]\n"
        "Ask questions and watch the agent solve them step by step!",
        border_style="cyan"
    ))
    console.print()
    
    agent = TodoAgent()
    
    while True:
        console.print()
        console.print("[bold yellow]Enter your question (or 'quit'/'exit' to stop):[/bold yellow]")
        user_question = Prompt.ask("[cyan]You[/cyan]")
        
        if user_question.lower() in ['quit', 'exit', 'q']:
            console.print("\n[bold green]Goodbye! 👋[/bold green]")
            break
        
        if not user_question.strip():
            console.print("[red]Please enter a question.[/red]")
            continue
        
        console.print()
        console.print(Panel.fit(
            f"[bold]Question:[/bold] {user_question}",
            border_style="blue"
        ))
        console.print()
        console.print("[dim]Agent is thinking and working...[/dim]\n")
        console.print("[dim]" + "="*60 + "[/dim]")
        
        try:
            # Run with verbose=True to see the execution live
            solution = agent.solve_problem(SYSTEM_MESSAGE, user_question, verbose=True)
            
            console.print()
            console.print("[dim]" + "="*60 + "[/dim]")
            console.print()
            console.print("[bold green]✅ Problem solved![/bold green]")
            console.print()
            
            # Show the final todo list
            console.print("[bold]Final Todo List:[/bold]")
            agent.show_tasks()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")
            console.print_exception()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted. Goodbye![/yellow]")
    except Exception as e:
        console.print(f"\n[red]Fatal error: {e}[/red]")
        console.print_exception()
