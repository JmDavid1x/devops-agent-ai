from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a chat message and return an AI-generated response.

    Currently returns a mock response. Will integrate with the AI provider later.
    """
    return ChatResponse(
        response=(
            "I'm the DevOps AI Agent. I can help you with "
            "log analysis, health checks, Docker management, and deployments."
        ),
        conversation_id=request.conversation_id or "mock-123",
        tools_used=[],
    )
