from datetime import datetime

from pydantic import BaseModel, Field


# Auth schemas
class UserCreate(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Chat schemas
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tools_used: list[str] = []


class ServiceConfigCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    url: str = Field(..., min_length=1, max_length=500)
    check_interval_seconds: int = Field(default=60, ge=10, le=3600)
    timeout_seconds: int = Field(default=10, ge=1, le=60)
    expected_status_code: int = Field(default=200, ge=100, le=599)


class ServiceConfigResponse(BaseModel):
    id: str
    name: str
    url: str
    check_interval_seconds: int
    timeout_seconds: int
    expected_status_code: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class HealthCheckResultResponse(BaseModel):
    id: str
    service_id: str
    status: str
    response_time_ms: float | None = None
    status_code: int | None = None
    error_message: str | None = None
    checked_at: datetime


class ServiceWithHealth(BaseModel):
    id: str
    name: str
    url: str
    status: str = "unknown"
    last_check: str | None = None
    response_time_ms: float | None = None
    is_active: bool = True


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
    state: str | None = None
    ports: list[str] = []
    cpu: str | None = None
    memory: str | None = None
    created: str | None = None


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
