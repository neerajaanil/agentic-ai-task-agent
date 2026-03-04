import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


class LLMClient:

    def __init__(self, model: str = "gpt-4.1-mini", api_key: str = None) -> None:
        # Use provided API key, or get from environment variable
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if api_key:
            self._client = OpenAI(api_key=api_key)
        else:
            # OpenAI will try to get from OPENAI_API_KEY env var automatically
            self._client = OpenAI()
        self._model = model

    def generate(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def chat(self, messages: list, tools: list = None) -> dict:
        """
        Generate a response from a list of messages (can include system, user, assistant roles).
        Supports function calling with tools.
        
        Returns:
            dict with 'message', 'finish_reason', and 'tool_calls' (if any)
        """
        kwargs = {
            "model": self._model,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools
            
        response = self._client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        
        return {
            "message": choice.message,
            "finish_reason": choice.finish_reason,
            "tool_calls": choice.message.tool_calls,
        }