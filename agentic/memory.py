from dataclasses import dataclass
from typing import List


@dataclass
class Todo:
    text: str
    completed: bool = False
    completion_notes: str = ""


class TodoMemory:

    def __init__(self) -> None:
        self._todos: List[Todo] = []

    def add(self, text: str) -> None:
        """Add a single todo item."""
        self._todos.append(Todo(text=text))

    def create_todos(self, descriptions: List[str]) -> str:
        """Add multiple todos from a list of descriptions and return the full list."""
        for desc in descriptions:
            self._todos.append(Todo(text=desc))
        return self.get_todo_report()

    def complete(self, index: int) -> None:
        """Mark a todo as complete (0-based index)."""
        if index < 0 or index >= len(self._todos):
            raise IndexError("Invalid todo index")
        self._todos[index].completed = True

    def mark_complete(self, index: int, completion_notes: str = "") -> str:
        """
        Mark a todo as complete (1-based index) with completion notes.
        Returns the todo report.
        """
        if 1 <= index <= len(self._todos):
            self._todos[index - 1].completed = True
            self._todos[index - 1].completion_notes = completion_notes
        else:
            return "No valid index at this point"
        return self.get_todo_report()

    def list(self) -> List[Todo]:
        """Get a list of all todos."""
        return list(self._todos)

    def report(self) -> str:
        """Get a simple text report of todos."""
        lines = []
        for i, todo in enumerate(self._todos):
            status = "✓" if todo.completed else " "
            lines.append(f"[{status}] {i+1}. {todo.text}")
        return "\n".join(lines)

    def get_todo_report(self) -> str:
        """Get a formatted todo report with Rich markup (returns string, not rendered)."""
        result = ""
        for index, todo in enumerate(self._todos):
            if todo.completed:
                result += f"Todo #{index + 1}: [green][strike]{todo.text}[/strike][/green]\n"
            else:
                result += f"Todo #{index + 1}: {todo.text}\n"
        return result