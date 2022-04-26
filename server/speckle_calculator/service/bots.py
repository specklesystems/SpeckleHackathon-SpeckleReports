import json
import requests
from devtools import debug
from dataclasses import dataclass

from specklepy.api.client import SpeckleClient

_COLOURS = {
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

_SPECKLE_LOGO = "https://avatars.githubusercontent.com/u/65039012?s=200&v=4"

_MESSAGE_TEMPLATE = {
    "username": "Speckle",
    "avatar_url": _SPECKLE_LOGO,
    "embeds": [
        {
            "author": {
                "name": "speckle user",
                "url": "",
                "icon_url": _SPECKLE_LOGO,
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


@dataclass
class DiscordCarbonNotifier:

    client: SpeckleClient
    stream_id: str
    commit_id: str
    discord_url: str
    report_url: str

    def _send_to_discord(self, message: dict):
        files = message.pop("files")
        files.append(("payload_json", (None, json.dumps(message))))
        res = requests.post(self.discord_url, files=files)
        debug(res)

    def __call__(self) -> None:

        stream = self.client.stream.get(self.stream_id)
        msg = _MESSAGE_TEMPLATE

        msg = _MESSAGE_TEMPLATE
        msg["embeds"][0].update(
            {
                "title": f"Carbon report ready in {stream.name}",
                "url": f"{self.client.url}/streams/{self.stream_id}/commits/{self.commit_id}",
                "description": f"Check the report at {self.report_url}/streams/{self.stream_id}/commits/{self.commit_id}",
                "color": _COLOURS["futures"],
                "fields": [],
            }
        )

        self._send_to_discord(msg)


@dataclass
class SlackCarbonNotifier:

    client: SpeckleClient
    stream_id: str
    commit_id: str
    slack_token: str
    slack_channel_id: str
    report_url: str

    def _send_to_slack(self, message: dict):
        res = requests.post("https://slack.com/api/chat.postMessage", json=message, headers={"Authorization": f"Bearer {self.slack_token}"})

        debug(res)

    def __call__(self) -> None:
        stream = self.client.stream.get(self.stream_id)
        payload = {
            "channel": self.slack_channel_id,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f'*Carbon Report Ready for "{stream.name}"*',
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Click the button to have a look!",
                    },
                    "accessory": {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "View Carbon Report",
                            "emoji": True,
                        },
                        "value": "click_me_123",
                        "url": f"{self.report_url}/streams/{self.stream_id}/commits/{self.commit_id}",
                        "action_id": "button-action",
                    },
                },
            ],
        }

        self._send_to_slack(payload)
