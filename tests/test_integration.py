import pytest
from unittest.mock import Mock, patch
from agentic.todo_agent import TodoAgent
from agentic.memory import TodoMemory


class TestIntegration:
    def test_agent_memory_integration(self):
        """Test that TodoAgent properly integrates with TodoMemory"""
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.Console'):
            agent = TodoAgent()
            
            # Add tasks through agent
            agent.add_task("Task 1")
            agent.add_task("Task 2")
            
            # Verify tasks are in memory
            todos = agent._memory.list()
            assert len(todos) == 2
            assert todos[0].text == "Task 1"
            assert todos[1].text == "Task 2"

    def test_agent_complete_integration(self):
        """Test completing tasks through agent"""
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.Console'):
            agent = TodoAgent()
            
            agent.add_task("Task 1")
            agent.add_task("Task 2")
            agent.complete_task(0)
            
            todos = agent._memory.list()
            assert todos[0].completed is True
            assert todos[1].completed is False

    def test_agent_show_tasks_integration(self):
        """Test showing tasks through agent"""
        with patch('agentic.todo_agent.LLMClient'), \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.add_task("Task 1")
            agent.add_task("Task 2")
            agent.show_tasks()
            
            # Verify console was called with report
            assert mock_console.print.called
            call_args = str(mock_console.print.call_args)
            assert "Task 1" in call_args or "Task 2" in call_args

    def test_agent_plan_tasks_integration(self):
        """Test planning tasks through agent"""
        with patch('agentic.todo_agent.LLMClient') as mock_llm_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_llm = Mock()
            mock_llm.generate.return_value = "Suggested plan: Do Task 1 first"
            mock_llm_class.return_value = mock_llm
            
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            agent.add_task("Task 1")
            agent.add_task("Task 2")
            agent.plan_tasks()
            
            # Verify LLM was called
            assert mock_llm.generate.called
            # Verify console printed the plan
            assert mock_console.print.call_count >= 2

    def test_full_workflow(self):
        """Test a complete workflow: add, show, complete, show, plan"""
        with patch('agentic.todo_agent.LLMClient') as mock_llm_class, \
             patch('agentic.todo_agent.Console') as mock_console_class:
            mock_llm = Mock()
            mock_llm.generate.return_value = "Plan: Complete remaining tasks"
            mock_llm_class.return_value = mock_llm
            
            mock_console = Mock()
            mock_console_class.return_value = mock_console
            
            agent = TodoAgent()
            
            # Add tasks
            agent.add_task("Buy groceries")
            agent.add_task("Write report")
            agent.add_task("Call dentist")
            
            # Show tasks
            agent.show_tasks()
            
            # Complete a task
            agent.complete_task(1)
            
            # Show tasks again
            agent.show_tasks()
            
            # Plan remaining tasks
            agent.plan_tasks()
            
            # Verify final state
            todos = agent._memory.list()
            assert len(todos) == 3
            assert todos[0].completed is False
            assert todos[1].completed is True
            assert todos[2].completed is False
            
            # Verify LLM was called for planning
            assert mock_llm.generate.called
