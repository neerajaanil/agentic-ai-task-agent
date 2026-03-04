import typer
from rich.console import Console
from .todo_agent import TodoAgent

app = typer.Typer()
console = Console()

SYSTEM_MESSAGE = """
You are given a problem to solve, by using your todo tools to plan a list of steps, then carrying out each step in turn.
Now use the todo list tools, create a plan, carry out the steps, and reply with the solution.
If any quantity isn't provided in the question, then include a step to come up with a reasonable estimate.
Provide your solution in Rich console markup without code blocks.
Do not ask the user questions or clarification; respond only with the answer after using your tools.
"""


@app.command()
def add(task: str):
    """Add a new task to the todo list."""
    agent = TodoAgent()
    agent.add_task(task)


@app.command()
def complete(index: int):
    """Mark a task as complete by its index (1-based)."""
    agent = TodoAgent()
    agent.complete_task(index - 1)


@app.command()
def list():
    """Show all tasks in the todo list."""
    agent = TodoAgent()
    agent.show_tasks()


@app.command()
def plan():
    """Get an AI-generated plan for completing tasks."""
    agent = TodoAgent()
    agent.plan_tasks()


@app.command()
def solve(question: str, verbose: bool = False):
    """
    Solve a problem using the todo agent with function calling.
    
    Example: python -m agentic.cli solve "A train leaves Boston at 2pm going 60mph..."
    """
    agent = TodoAgent()
    agent.solve_problem(SYSTEM_MESSAGE, question, verbose=verbose)


@app.command()
def demo():
    """Run an interactive demo where you can ask questions."""
    import sys
    from pathlib import Path
    from rich.panel import Panel
    from rich.prompt import Prompt
    
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    
    from examples.interactive_demo import main
    main()


if __name__ == "__main__":
    app()