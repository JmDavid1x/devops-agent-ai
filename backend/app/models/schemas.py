from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tools_used: list[str] = []


class Service(BaseModel):
    id: str
    name: str
    url: str
    status: str
    last_check: str | None = None


class Container(BaseModel):
    id: str
    name: str
    image: str
    status: str
    ports: list[str] = []


class HealthCheck(BaseModel):
    service_id: str
    status: str
    response_time_ms: float
    timestamp: str


class MessageSchema(BaseModel):
    id: str
    role: str
    content: str
    tools_used: list[str] | None = None
    created_at: datetime


class ConversationSchema(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageSchema] = []


class ConversationListItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
