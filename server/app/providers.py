from typing import Dict
from app.webhook_handler_registry import WebhookHandlerRegistry
import os


def speckle_token_provider() -> Dict[str, str]:
    return {os.environ["SPECKLE_SERVER_URL"]: os.environ["SPECKLE_TOKEN"]}


def webhook_registry() -> WebhookHandlerRegistry:
    return WebhookHandlerRegistry(
        speckle_token_provider(),
        os.environ["DISCORD_URL"],
        os.environ["REPORT_URL"],
    )
