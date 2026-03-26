from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DevOps AI Agent"
    debug: bool = False
    api_version: str = "v1"
    claude_api_key: str = ""
    openai_api_key: str = ""
    ai_provider: str = "claude"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/devops_agent"
    redis_url: str = "redis://localhost:6379/0"

    model_config = {"env_file": ".env"}


settings = Settings()
