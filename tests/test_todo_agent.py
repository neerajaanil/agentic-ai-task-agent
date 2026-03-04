import pytest
from unittest.mock import Mock, patch, MagicMock
from agentic.todo_agent import TodoAgent


class TestTodoAgent:
    def test_initialization_default_model(self):
        with patch('agentic.todo_agent.LLMClient') as mock_llm, \
             patch('agentic.todo_agent.TodoMemory') as mock_memory, \
             patch('agentic.todo_agent.Console') as mock_console:
            agent = TodoAgent()
            assert agent._llm is not None
            assert agent._memory is not None
            assert agent._console is not None
            mock_llm.assert_called_once_with(model="gpt-4.1-mini")

    def test_initialization_custom_model(self):
        with patch('agentic.todo_agent.LLMClient') as mock_llm, \
             patch('agentic.todo_agent.TodoMemory') as mock_memory, \
             patch('agentic.todo_agent.Console') as mock_console:
            agent = TodoAgent(model="gpt-4")
            mock_llm.assert_called_once_with(model="gpt-4")

    def test_add_task(self):
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_memory = Mock()
            mock_memory_class.return_value = mock_memory
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.add_task("Buy groceries")
            
            mock_memory.add.assert_called_once_with("Buy groceries")
            mock_console.print.assert_called_once()

    def test_complete_task(self):
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_memory = Mock()
            mock_memory_class.return_value = mock_memory
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.complete_task(0)
            
            mock_memory.complete.assert_called_once_with(0)
            mock_console.print.assert_called_once()

    def test_show_tasks_with_tasks(self):
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_memory = Mock()
            mock_memory.report.return_value = "[ ] 1. Task 1"
            mock_memory_class.return_value = mock_memory
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.show_tasks()
            
            mock_memory.report.assert_called_once()
            mock_console.print.assert_called_once_with("[ ] 1. Task 1")

    def test_show_tasks_empty(self):
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_memory = Mock()
            mock_memory.report.return_value = ""
            mock_memory_class.return_value = mock_memory
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.show_tasks()
            
            mock_memory.report.assert_called_once()
            mock_console.print.assert_called_once_with("No tasks.")

    def test_plan_tasks(self):
        with patch('agentic.todo_agent.LLMClient') as mock_llm_class, \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_memory = Mock()
            mock_memory.report.return_value = "[ ] 1. Task 1\n[ ] 2. Task 2"
            mock_memory_class.return_value = mock_memory
            
            mock_llm = Mock()
            mock_llm.generate.return_value = "Plan: Do Task 1 first, then Task 2"
            mock_llm_class.return_value = mock_llm
            
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.plan_tasks()
            
            mock_memory.report.assert_called_once()
            mock_llm.generate.assert_called_once()
            assert mock_console.print.call_count == 2  # Once for header, once for plan

    def test_plan_tasks_prompt_format(self):
        with patch('agentic.todo_agent.LLMClient') as mock_llm_class, \
             patch('agentic.todo_agent.TodoMemory') as mock_memory_class, \
             patch('agentic.todo_agent.Console'):
            mock_memory = Mock()
            mock_memory.report.return_value = "[ ] 1. Task 1"
            mock_memory_class.return_value = mock_memory
            
            mock_llm = Mock()
            mock_llm.generate.return_value = "Test plan"
            mock_llm_class.return_value = mock_llm
            
            agent = TodoAgent()
            agent.plan_tasks()
            
            call_args = mock_llm.generate.call_args[0][0]
            assert "productivity assistant" in call_args.lower()
            assert "Task 1" in call_args
            assert "order to complete" in call_args.lower()
