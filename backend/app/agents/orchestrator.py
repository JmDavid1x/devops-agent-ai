import json
import logging

from app.core.ai_provider import AIProvider, get_ai_provider
from app.agents.tools import ALL_TOOLS
from app.agents.tool_executor import execute_tool

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a DevOps AI Agent that helps engineers manage infrastructure,
analyze logs, monitor services, and handle deployments.

You have access to the following tools to interact with the infrastructure:
- analyze_logs: Analyze application logs for errors and anomalies
- check_service_health: Check health status of services
- list_containers: List Docker containers and their status
- restart_container: Restart a Docker container
- deploy_service: Deploy or update a service

When a user asks about infrastructure, services, or deployments, use the appropriate tools
to gather real data before responding. Always provide actionable insights based on the data.
If you don't need a tool, respond directly with helpful information."""

MAX_TOOL_ROUNDS = 5  # prevent infinite loops


class AgentOrchestrator:
    def __init__(self, provider: AIProvider | None = None):
        self.provider = provider or get_ai_provider()
        self.tools_used: list[str] = []

    async def run(self, user_message: str, history: list[dict] | None = None) -> dict:
        """Run the agent loop.

        Args:
            user_message: The user's message
            history: Optional conversation history (list of {"role": ..., "content": ...})

        Returns:
            dict with "content" (str), "tools_used" (list[str])
        """
        messages = []

        # Add system message (for OpenAI style; Claude uses system param differently but our adapter handles it)
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

        # Add history
        if history:
            messages.extend(history)

        # Add new user message
        messages.append({"role": "user", "content": user_message})

        self.tools_used = []

        for round_num in range(MAX_TOOL_ROUNDS):
            logger.info(f"Agent round {round_num + 1}")

            response = await self.provider.chat(messages=messages, tools=ALL_TOOLS)

            tool_calls = response.get("tool_calls", [])
            content = response.get("content", "")

            if not tool_calls:
                # No tools called - we have a final response
                return {
                    "content": content,
                    "tools_used": self.tools_used,
                }

            # Add assistant message with tool calls to history
            messages.append({
                "role": "assistant",
                "content": content,
                "tool_calls": tool_calls,
            })

            # Execute each tool and add results
            for tc in tool_calls:
                tool_name = tc["name"]
                tool_args = tc["arguments"]

                # OpenAI returns arguments as JSON string, Claude as dict
                if isinstance(tool_args, str):
                    tool_args = json.loads(tool_args)

                logger.info(f"Executing tool: {tool_name} with args: {tool_args}")

                result = await execute_tool(tool_name, tool_args)
                self.tools_used.append(tool_name)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "name": tool_name,
                    "content": json.dumps(result),
                })

        # If we hit max rounds, return what we have
        return {
            "content": content or "I've reached the maximum number of tool rounds. Here's what I found so far.",
            "tools_used": self.tools_used,
        }
