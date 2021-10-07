from importlib.metadata import version

from fastapi import FastAPI, Depends
from fastapi.background import BackgroundTasks

import speckle_calculator

from app.webhook_handler_registry import WebhookHandlerRegistry
from app.providers import webhook_registry
from app.models import Webhook


app = FastAPI()


@app.get("/healt")
async def health():
    return True


@app.get("/version")
async def get_version():
    return version(speckle_calculator.__name__)


@app.post("/calculate")
async def calculate(
    webhook_data: dict,
    background_tasks: BackgroundTasks,
    webhook_handler_registry: WebhookHandlerRegistry = Depends(webhook_registry),
) -> str:

    payload = webhook_data["payload"]

    # this is here to ease testing without double string encoded payload.
    if isinstance(payload, dict):
        import json

        payload = json.dumps(payload)

    webhook = Webhook.parse_raw(payload)

    if handler := webhook_handler_registry(webhook):
        background_tasks.add_task(handler)
        return "On it."

    else:
        return "No handlers registered for this hook."
