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
        # Extract system messages and remove them from the messages list
        system_parts: list[str] = []
        filtered_messages: list[dict] = []

        for msg in messages:
            if msg["role"] == "system":
                system_parts.append(msg["content"])
            else:
                filtered_messages.append(msg)

        # Convert messages to Claude's expected format
        claude_messages: list[dict] = []
        for msg in filtered_messages:
            if msg["role"] == "assistant" and "tool_calls" in msg:
                # Convert assistant tool_calls to Claude's tool_use content blocks
                content_blocks: list[dict] = []
                if msg.get("content"):
                    content_blocks.append({"type": "text", "text": msg["content"]})
                for tc in msg["tool_calls"]:
                    content_blocks.append({
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": tc["name"],
                        "input": tc["arguments"] if isinstance(tc["arguments"], dict) else {},
                    })
                claude_messages.append({"role": "assistant", "content": content_blocks})
            elif msg["role"] == "tool":
                # Convert tool results to Claude's tool_result content blocks
                claude_messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": msg["tool_call_id"],
                            "content": msg["content"],
                        }
                    ],
                })
            else:
                claude_messages.append({"role": msg["role"], "content": msg["content"]})

        kwargs: dict = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": claude_messages,
        }

        if system_parts:
            kwargs["system"] = "\n\n".join(system_parts)

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
        # Convert messages to OpenAI's expected format
        openai_messages: list[dict] = []

        for msg in messages:
            if msg["role"] == "assistant" and "tool_calls" in msg:
                # Convert to OpenAI's tool_calls format
                oai_tool_calls = [
                    {
                        "id": tc["id"],
                        "type": "function",
                        "function": {
                            "name": tc["name"],
                            "arguments": tc["arguments"] if isinstance(tc["arguments"], str) else "{}",
                        },
                    }
                    for tc in msg["tool_calls"]
                ]
                openai_messages.append({
                    "role": "assistant",
                    "content": msg.get("content") or None,
                    "tool_calls": oai_tool_calls,
                })
            elif msg["role"] == "tool":
                openai_messages.append({
                    "role": "tool",
                    "tool_call_id": msg["tool_call_id"],
                    "content": msg["content"],
                })
            else:
                openai_messages.append({"role": msg["role"], "content": msg["content"]})

        kwargs: dict = {
            "model": self.model,
            "messages": openai_messages,
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
