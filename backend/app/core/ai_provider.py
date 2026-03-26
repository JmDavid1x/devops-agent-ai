from abc import ABC, abstractmethod

import anthropic
import openai

from app.core.config import settings


class AIProvider(ABC):
    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        """Send a chat request and return the response.

        Args:
            messages: List of message dicts with 'role' and 'content'.
            tools: Optional list of tool/function definitions.

        Returns:
            Dict with 'content' (str) and optionally 'tool_calls' (list).
        """
        ...


class ClaudeProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        kwargs: dict = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": messages,
        }

        if tools:
            claude_tools = [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "input_schema": t["parameters"],
                }
                for t in tools
            ]
            kwargs["tools"] = claude_tools

        response = await self.client.messages.create(**kwargs)

        content = ""
        tool_calls: list[dict] = []
        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    {
                        "id": block.id,
                        "name": block.name,
                        "arguments": block.input,
                    }
                )

        result: dict = {"content": content}
        if tool_calls:
            result["tool_calls"] = tool_calls
        return result


class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str) -> None:
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4o"

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict] | None = None,
    ) -> dict:
        kwargs: dict = {
            "model": self.model,
            "messages": messages,
        }

        if tools:
            openai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t["description"],
                        "parameters": t["parameters"],
                    },
                }
                for t in tools
            ]
            kwargs["tools"] = openai_tools

        response = await self.client.chat.completions.create(**kwargs)
        message = response.choices[0].message

        result: dict = {"content": message.content or ""}

        if message.tool_calls:
            tool_calls = [
                {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                }
                for tc in message.tool_calls
            ]
            result["tool_calls"] = tool_calls

        return result


def get_ai_provider(provider: str | None = None) -> AIProvider:
    """Factory function to create the appropriate AI provider.

    Args:
        provider: 'claude' or 'openai'. Defaults to settings.ai_provider.

    Returns:
        An AIProvider instance.
    """
    provider = provider or settings.ai_provider

    if provider == "claude":
        return ClaudeProvider(api_key=settings.claude_api_key)
    elif provider == "openai":
        return OpenAIProvider(api_key=settings.openai_api_key)
    else:
        raise ValueError(f"Unknown AI provider: {provider}")
