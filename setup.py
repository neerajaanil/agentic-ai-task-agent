from setuptools import setup, find_packages

setup(
    name="agentic-ai-task-agent",
    version="0.1.0",
    description="A production-ready Python AI agent that manages tasks, maintains memory, and uses LLM planning.",
    packages=find_packages(),
    install_requires=[
        "openai",
        "rich",
        "typer",
        "python-dotenv",
    ],
    python_requires=">=3.8",
)
