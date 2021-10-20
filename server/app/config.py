from dataclasses import dataclass
from pydantic import BaseSettings
from functools import lru_cache
from app.webhook_handler_registry import WebhookHandlerRegistry


class Settings(BaseSettings):
    speckle_token: str
    discord_url: str
    speckle_server_url: str
    result_url: str
    slack_token: str
    slack_channel_id: str

    class Config:
        env_file = ".env"


@lru_cache()
def webhook_registry() -> WebhookHandlerRegistry:
    settings = Settings()

    return WebhookHandlerRegistry(
        {settings.speckle_server_url: settings.speckle_token},
        settings.discord_url,
        settings.result_url,
        settings.slack_token,
        settings.slack_channel_id,
    )
