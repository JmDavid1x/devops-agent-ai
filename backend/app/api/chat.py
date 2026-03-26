import json
import uuid
import logging

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import AgentOrchestrator
from app.core.database import get_db
from app.models.db_models import Conversation, Message
from app.models.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


async def _get_or_create_conversation(
    db: AsyncSession,
    conversation_id: str | None,
) -> Conversation:
    """Get existing conversation or create a new one."""
    if conversation_id:
        stmt = select(Conversation).where(
            Conversation.id == uuid.UUID(conversation_id)
        )
        result = await db.execute(stmt)
        conv = result.scalar_one_or_none()
        if conv:
            return conv

    conv = Conversation()
    db.add(conv)
    await db.flush()
    return conv


async def _get_history(db: AsyncSession, conversation_id: uuid.UUID) -> list[dict]:
    """Get conversation history formatted for the AI provider."""
    stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    result = await db.execute(stmt)
    messages = result.scalars().all()

    return [{"role": m.role, "content": m.content} for m in messages]


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Process a chat message using the AI agent."""
    try:
        # Get or create conversation
        conv = await _get_or_create_conversation(db, request.conversation_id)

        # Get history
        history = await _get_history(db, conv.id)

        # Save user message
        user_msg = Message(
            conversation_id=conv.id,
            role="user",
            content=request.message,
        )
        db.add(user_msg)
        await db.flush()

        # Run agent
        orchestrator = AgentOrchestrator()
        result = await orchestrator.run(
            user_message=request.message,
            history=history,
        )

        # Save assistant response
        assistant_msg = Message(
            conversation_id=conv.id,
            role="assistant",
            content=result["content"],
            tools_used=result["tools_used"] if result["tools_used"] else None,
        )
        db.add(assistant_msg)

        # Update conversation title from first message
        if not history:
            conv.title = request.message[:100]

        await db.commit()

        return ChatResponse(
            response=result["content"],
            conversation_id=str(conv.id),
            tools_used=result["tools_used"],
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        await db.rollback()
        # Fallback: return error as response instead of crashing
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}. Make sure the AI provider API key is configured.",
            conversation_id=request.conversation_id or str(uuid.uuid4()),
            tools_used=[],
        )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """Stream chat response via Server-Sent Events."""

    async def event_generator():
        try:
            conv = await _get_or_create_conversation(db, request.conversation_id)

            yield f"data: {json.dumps({'type': 'conversation_id', 'data': str(conv.id)})}\n\n"

            history = await _get_history(db, conv.id)

            user_msg = Message(
                conversation_id=conv.id,
                role="user",
                content=request.message,
            )
            db.add(user_msg)
            await db.flush()

            yield f"data: {json.dumps({'type': 'status', 'data': 'thinking'})}\n\n"

            orchestrator = AgentOrchestrator()
            result = await orchestrator.run(
                user_message=request.message,
                history=history,
            )

            if result["tools_used"]:
                yield f"data: {json.dumps({'type': 'tools_used', 'data': result['tools_used']})}\n\n"

            yield f"data: {json.dumps({'type': 'content', 'data': result['content']})}\n\n"

            assistant_msg = Message(
                conversation_id=conv.id,
                role="assistant",
                content=result["content"],
                tools_used=result["tools_used"] if result["tools_used"] else None,
            )
            db.add(assistant_msg)

            if not history:
                conv.title = request.message[:100]

            await db.commit()

            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
