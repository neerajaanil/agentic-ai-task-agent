import pytest
from agentic.memory import TodoMemory, Todo


class TestTodo:
    def test_todo_creation(self):
        todo = Todo(text="Test task")
        assert todo.text == "Test task"
        assert todo.completed is False

    def test_todo_with_completed(self):
        todo = Todo(text="Done task", completed=True)
        assert todo.text == "Done task"
        assert todo.completed is True


class TestTodoMemory:
    def test_initialization(self):
        memory = TodoMemory()
        assert memory.list() == []

    def test_add_task(self):
        memory = TodoMemory()
        memory.add("Buy groceries")
        todos = memory.list()
        assert len(todos) == 1
        assert todos[0].text == "Buy groceries"
        assert todos[0].completed is False

    def test_add_multiple_tasks(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        memory.add("Task 3")
        todos = memory.list()
        assert len(todos) == 3
        assert todos[0].text == "Task 1"
        assert todos[1].text == "Task 2"
        assert todos[2].text == "Task 3"

    def test_complete_task(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        memory.complete(0)
        todos = memory.list()
        assert todos[0].completed is True
        assert todos[1].completed is False

    def test_complete_task_invalid_index_negative(self):
        memory = TodoMemory()
        memory.add("Task 1")
        with pytest.raises(IndexError, match="Invalid todo index"):
            memory.complete(-1)

    def test_complete_task_invalid_index_too_large(self):
        memory = TodoMemory()
        memory.add("Task 1")
        with pytest.raises(IndexError, match="Invalid todo index"):
            memory.complete(1)

    def test_complete_task_empty_list(self):
        memory = TodoMemory()
        with pytest.raises(IndexError, match="Invalid todo index"):
            memory.complete(0)

    def test_list_todos(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        todos = memory.list()
        assert isinstance(todos, list)
        assert len(todos) == 2
        assert all(isinstance(todo, Todo) for todo in todos)

    def test_report_empty(self):
        memory = TodoMemory()
        report = memory.report()
        assert report == ""

    def test_report_single_task(self):
        memory = TodoMemory()
        memory.add("Buy milk")
        report = memory.report()
        assert "[ ] 1. Buy milk" in report

    def test_report_multiple_tasks(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        memory.add("Task 3")
        report = memory.report()
        assert "[ ] 1. Task 1" in report
        assert "[ ] 2. Task 2" in report
        assert "[ ] 3. Task 3" in report

    def test_report_with_completed_tasks(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        memory.complete(0)
        report = memory.report()
        assert "[✓] 1. Task 1" in report
        assert "[ ] 2. Task 2" in report

    def test_report_all_completed(self):
        memory = TodoMemory()
        memory.add("Task 1")
        memory.add("Task 2")
        memory.complete(0)
        memory.complete(1)
        report = memory.report()
        assert "[✓] 1. Task 1" in report
        assert "[✓] 2. Task 2" in report
