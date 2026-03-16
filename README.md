# 🤖 Agentic AI Task Agent

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A production-ready Python AI agent that demonstrates advanced **agentic AI systems** capabilities through autonomous task planning, execution, and memory management using OpenAI Agents SDK

## 🌟 Overview

This project showcases a sophisticated **agentic AI system** that autonomously:
- **Plans** complex problems by breaking them into actionable steps
- **Executes** tasks sequentially using function calling
- **Maintains memory** of completed and pending tasks
- **Adapts** its approach based on intermediate results

Unlike simple chatbots, this agent uses **OpenAI function calling** to interact with its own toolset, creating a feedback loop where the LLM can plan, execute, and iterate on solutions autonomously.

## 🎯 Key Features

### Agentic Capabilities
- **Autonomous Planning**: Breaks down complex problems into step-by-step todo lists
- **Function Calling**: Uses OpenAI's function calling API to interact with tools
- **Iterative Execution**: Executes tasks sequentially and adapts based on results
- **Memory Management**: Maintains persistent state across multiple tool interactions
- **Self-Directed Problem Solving**: Makes decisions about task order and execution

### Technical Features
- **Production-Ready Code**: Clean architecture with separation of concerns
- **Rich CLI Interface**: Beautiful terminal UI using Rich library
- **Comprehensive Testing**: Full test coverage with pytest
- **Type Hints**: Full type annotations for better code quality
- **Environment Management**: Secure API key handling with python-dotenv

## 🏗️ Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐
│   TodoAgent      │  ← Orchestrates the agentic workflow
│  (Orchestrator)  │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐  ┌─▼────┐
│Memory │  │ LLM  │
│       │  │Client│
└───────┘  └──────┘
```

### Core Components

1. **`TodoAgent`**: Main orchestrator that manages the agentic workflow
   - Handles function calling loop
   - Manages tool execution
   - Coordinates between memory and LLM

2. **`TodoMemory`**: Persistent memory system
   - Stores task state (pending/completed)
   - Tracks completion notes
   - Provides formatted reports

3. **`LLMClient`**: OpenAI API wrapper
   - Handles chat completions
   - Manages function calling
   - Supports multiple models

4. **Tools**: Function calling interface
   - `create_todos`: Add multiple tasks to the plan
   - `mark_complete`: Mark tasks as done with notes

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/neerajaanil/agentic-ai-task-agent.git
   cd agentic-ai-task-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Install the package** (optional but recommended)
   ```bash
   pip install -e .
   ```

## 💡 Usage

### Interactive Demo (Recommended)

Experience the agentic system in action with the interactive demo:

```bash
python examples/interactive_demo.py
```

Or use the CLI:
```bash
python -m agentic.cli demo
```

**Example Session:**
```
🤖 Todo Agent Interactive Demo

Enter your question:
You: A train leaves Boston at 2pm going 60mph. Another train leaves New York at 3pm going 80mph toward Boston. When do they meet?

[Agent creates todos, executes steps, and solves the problem]
✅ Problem solved!
```

### Command Line Interface

**Basic Todo Management:**
```bash
# Add a task
python -m agentic.cli add "Buy groceries"

# List all tasks
python -m agentic.cli list

# Mark task as complete
python -m agentic.cli complete 1

# Get AI-generated plan
python -m agentic.cli plan
```

**Solve Problems with Function Calling:**
```bash
python -m agentic.cli solve "Your problem here" --verbose
```

### Programmatic Usage

```python
from agentic.todo_agent import TodoAgent

# Initialize the agent
agent = TodoAgent()

# Solve a problem using agentic workflow
system_message = """
You are given a problem to solve, by using your todo tools to plan 
a list of steps, then carrying out each step in turn.
"""

user_message = "A train leaves Boston at 2pm going 60mph..."

solution = agent.solve_problem(system_message, user_message, verbose=True)
```

## 🔬 How It Works: The Agentic Loop

The system implements a sophisticated agentic loop:

1. **Problem Reception**: Agent receives a problem statement
2. **Planning Phase**: LLM uses `create_todos` tool to break down the problem
3. **Execution Phase**: LLM uses `mark_complete` tool to execute each step
4. **Iteration**: Agent continues until all steps are complete
5. **Solution Generation**: Final answer is provided with reasoning

```
User Question
    ↓
[LLM analyzes problem]
    ↓
[Creates todos via function calling]
    ↓
[Executes each todo step by step]
    ↓
[Adapts based on intermediate results]
    ↓
Final Solution
```

## 📁 Project Structure

```
agentic-ai-task-agent/
├── agentic/
│   ├── __init__.py          # Package initialization
│   ├── todo_agent.py        # Main agent orchestrator
│   ├── memory.py            # Memory management system
│   ├── llm.py               # OpenAI API client
│   └── cli.py               # Command-line interface
├── examples/
│   ├── run_agent.py         # Basic example
│   └── interactive_demo.py  # Interactive demo
├── tests/
│   ├── test_memory.py       # Memory tests
│   ├── test_llm.py          # LLM client tests
│   ├── test_todo_agent.py   # Agent tests
│   └── test_integration.py  # Integration tests
├── requirements.txt         # Dependencies
├── setup.py                 # Package setup
└── README.md                # This file
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=agentic --cov-report=html

# Run specific test file
pytest tests/test_todo_agent.py
```

The test suite includes:
- Unit tests for each component
- Integration tests for the full workflow
- Mocked API calls for reliable testing
- Edge case handling

## 🛠️ Technical Stack

- **Python 3.8+**: Modern Python with type hints
- **OpenAI API**: GPT-4o-mini for LLM capabilities
- **Function Calling**: OpenAI's function calling API
- **Rich**: Beautiful terminal output
- **Typer**: Modern CLI framework
- **pytest**: Testing framework
- **python-dotenv**: Environment variable management

## 🎓 What Makes This Agentic?

This project demonstrates **true agentic AI** through:

1. **Autonomous Decision Making**: The agent decides what steps to take
2. **Tool Usage**: Uses function calling to interact with its environment
3. **State Management**: Maintains memory across multiple interactions
4. **Iterative Refinement**: Can adapt its plan based on results
5. **Goal-Oriented Behavior**: Works towards solving the given problem

Unlike simple prompt engineering, this system creates a **feedback loop** where:
- The LLM can observe the results of its actions
- It can modify its approach based on intermediate states
- It maintains context across multiple tool calls
- It autonomously determines when the task is complete

## 📝 Example Use Cases

- **Mathematical Problem Solving**: Break down complex calculations
- **Planning Tasks**: Create and execute multi-step plans
- **Research Questions**: Plan research steps and execute them
- **Code Generation Planning**: Plan software development tasks
- **Data Analysis**: Plan analysis steps and execute sequentially

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Inspired by**: [AI Engineer Agentic Track: The Complete Agent & MCP Course](https://www.udemy.com/) on Udemy
- OpenAI for the powerful GPT models and function calling API
- The Rich library for beautiful terminal output
- The Python community for excellent tooling

## 📧 Contact

- **LinkedIn**: [Neeraja Anil](https://www.linkedin.com/in/neeraja-anil/)
- **GitHub**: [@neerajaanil](https://github.com/neerajaanil)

For questions or feedback, please open an issue on [GitHub](https://github.com/neerajaanil/agentic-ai-task-agent/issues) or reach out via LinkedIn.

---

**Built with ❤️ to demonstrate agentic AI systems capabilities**
