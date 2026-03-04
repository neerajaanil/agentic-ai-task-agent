import pytest
from unittest.mock import Mock, patch
from agentic.llm import LLMClient


class TestLLMClient:
    def test_initialization_default_model(self):
        with patch('agentic.llm.OpenAI') as mock_openai:
            client = LLMClient()
            assert client._model == "gpt-4.1-mini"
            mock_openai.assert_called_once()

    def test_initialization_custom_model(self):
        with patch('agentic.llm.OpenAI') as mock_openai:
            client = LLMClient(model="gpt-4")
            assert client._model == "gpt-4"
            mock_openai.assert_called_once()

    def test_generate(self):
        with patch('agentic.llm.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            
            llm = LLMClient()
            result = llm.generate("Test prompt")
            
            assert result == "Test response"
            mock_client.chat.completions.create.assert_called_once_with(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": "Test prompt"}]
            )

    def test_generate_with_custom_model(self):
        with patch('agentic.llm.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Custom model response"
            mock_client.chat.completions.create.return_value = mock_response
            
            llm = LLMClient(model="gpt-4")
            result = llm.generate("Test prompt")
            
            assert result == "Custom model response"
            mock_client.chat.completions.create.assert_called_once_with(
                model="gpt-4",
                messages=[{"role": "user", "content": "Test prompt"}]
            )

    def test_generate_empty_prompt(self):
        with patch('agentic.llm.OpenAI') as mock_openai_class:
            mock_client = Mock()
            mock_openai_class.return_value = mock_client
            
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = ""
            mock_client.chat.completions.create.return_value = mock_response
            
            llm = LLMClient()
            result = llm.generate("")
            
            assert result == ""
            mock_client.chat.completions.create.assert_called_once()
