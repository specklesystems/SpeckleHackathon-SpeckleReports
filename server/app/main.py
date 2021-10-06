from typing import Any
from fastapi import FastAPI, Depends
from fastapi.background import BackgroundTasks
from specklepy import objects
from specklepy.api.client import SpeckleClient
from specklepy.objects.base import Base
from specklepy.transports.server.server import ServerTransport
from speckle_calculator.service import carbon, discord
from app.transport_provider import speckle_token_provider


from pydantic import BaseModel, Field
from devtools import debug
import stringcase


app = FastAPI()


class CarbonBase(BaseModel):
    """Carbon base model"""

    class Config:
        alias_generator = stringcase.camelcase


class Commit(CarbonBase):
    stream_id: str
    branch_name: str
    source_application: str
    message: str
    object_id: str


class CommitCreateData(CarbonBase):
    id: str
    commit: Commit


class CommitCreateEvent(BaseModel):
    event_name: str
    data: CommitCreateData


class ServerData(CarbonBase):

    canonical_url: str


class Webhook(CarbonBase):
    """Data structure for a commit create event."""

    stream_id: str
    user_id: str
    activity_message: str
    event: CommitCreateEvent
    server: ServerData


class WebhookWrapper(Webhook):

    payload: str


def _create_carbon_input(webhook: Webhook) -> carbon.CarbonInput:
    return carbon.CarbonInput(
        webhook.stream_id,
        webhook.event.data.commit.object_id,
    )


def _create_chatbot_input(webhook: Webhook) -> discord.DiscordInput:
    return discord.DiscordInput(
        webhook.server.canonical_url,
        webhook.stream_id,
        "http://localhost:8080/",
        "https://discord.com/api/webhooks/889904023782694952/MK0_i9aI-DKStrAvgk7hzctw3tt0mKRq8rBN27DFKlUPL8mbBGF326C2f106RRNIm4UI",
    )


_registered_handlers = {
    "main": {"input_creator": _create_carbon_input, "solver": carbon.calculate_carbon},
    "carbon-results": {
        "input_creator": _create_chatbot_input,
        "solver": discord.on_commit_create,
    },
}


@app.post("/calculate")
async def calculate(
    webhook_data: dict,
    background_tasks: BackgroundTasks,
    speckle_token: str = Depends(speckle_token_provider),
) -> str:

    payload = webhook_data["payload"]

    # cause of input format... talk to Dim about this
    if isinstance(payload, dict):
        import json

        payload = json.dumps(payload)

    webhook = Webhook.parse_raw(payload)

    if handler := _registered_handlers.get(webhook.event.data.commit.branch_name):
        client = SpeckleClient(host=webhook.server.canonical_url, use_ssl=False)
        client.authenticate(speckle_token)
        transport = ServerTransport(client, webhook.stream_id)

        input = handler["input_creator"](webhook)
        solver = handler["solver"]

        background_tasks.add_task(
            solver,
            input,
            transport,
            client,
        )
        return "On it."

    else:
        return "I'll pass."
