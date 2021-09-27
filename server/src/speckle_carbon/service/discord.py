import json
import requests
from devtools import debug
from dataclasses import dataclass

from specklepy.api.client import SpeckleClient


COLOURS = {
    "speckle blue": 295163,
    "spark": 119293,
    "futures": 9011703,
    "funk": 6771167,
    "majestic": 2960090,
    "lightning": 14204694,
    "data yellow": 16508501,
    "twist": 6872905,
    "mantis": 2266732,
    "flavour": 12999895,
    "environment": 11469515,
    "red": 16532034,
}

SPECKLE_LOGO = "https://avatars.githubusercontent.com/u/65039012?s=200&v=4"

MESSAGE_TEMPLATE = {
    "username": "Speckle",
    "avatar_url": SPECKLE_LOGO,
    "embeds": [
        {
            "author": {
                "name": "speckle user",
                "url": "",
                "icon_url": SPECKLE_LOGO,
            },
            "title": "",
            "url": "",
            "description": "",
            "color": 295163,
            "image": {"url": None},
        }
    ],
    "files": [],
}


@dataclass
class DiscordInput:
    server_url: str
    stream_id: str
    carbon_url: str
    discord_url: str


def send_to_discord(discord_url: str, message: str):
    files = message.pop("files")
    debug(message)
    files.append(("payload_json", (None, json.dumps(message))))
    res = requests.post(discord_url, files=files)
    debug(res)


def on_commit_create(discord_input: DiscordInput, transport, client: SpeckleClient):
    stream = client.stream.get(discord_input.stream_id)

    stream.name

    msg = MESSAGE_TEMPLATE
    msg["embeds"][0].update(
        {
            "title": f"Carbon report ready in {stream.name}",
            "url": f"{discord_input.server_url}/streams/{discord_input.stream_id}/branches/main",
            "description": f"Check the report at {discord_input.carbon_url}/streams/{discord_input.stream_id}",
            "color": COLOURS["futures"],
            "fields": [],
        }
    )

    send_to_discord(discord_input.discord_url, msg)
