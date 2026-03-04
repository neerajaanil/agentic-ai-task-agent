import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agentic.todo_agent import TodoAgent

# Example: Solve a problem using the todo agent
system_message = """
You are given a problem to solve, by using your todo tools to plan a list of steps, then carrying out each step in turn.
Now use the todo list tools, create a plan, carry out the steps, and reply with the solution.
If any quantity isn't provided in the question, then include a step to come up with a reasonable estimate.
Provide your solution in Rich console markup without code blocks.
Do not ask the user questions or clarification; respond only with the answer after using your tools.
"""

user_message = """
A train leaves Boston at 2:00 pm traveling 60 mph.
Another train leaves New York at 3:00 pm traveling 80 mph toward Boston.
When do they meet?
"""

if __name__ == "__main__":
    agent = TodoAgent()
    
    # Solve the problem with function calling
    # Set verbose=True to see message trace (like in the notebook)
    solution = agent.solve_problem(system_message, user_message, verbose=False)
    
    # Optionally show any tasks that were created during planning
    agent.show_tasks()
