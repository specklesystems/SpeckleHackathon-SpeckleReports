from dataclasses import dataclass
from typing import Callable, Dict, Optional

from specklepy.api.client import SpeckleClient
from speckle_calculator.service import carbon, bots

from app.models import Webhook

from devtools import debug


@dataclass
class WebhookHandlerRegistry:

    _token_registry: Dict[str, str]
    _discord_url: str
    _report_url: str
    _slack_token: str
    _slack_channel_id: str
    _tracked_branch: str = "main"
    _result_branch: str = "carbon-results"

    def __call__(self, webhook: Webhook) -> Optional[Callable[[None], None]]:
        branch_name = webhook.event.data.commit.branch_name
        server_url = webhook.server.canonical_url.rstrip("/")
        debug(webhook)
        if token := self._token_registry.get(server_url):
            client = SpeckleClient(
                host=webhook.server.canonical_url,
                use_ssl=server_url.startswith("https://"),
            )
            client.authenticate(token)
        else:
            raise ValueError(
                f"The application is not authorized on {server_url} server"
            )

        if branch_name == self._tracked_branch:
            # calculate carbon!
            return carbon.CarbonCalculator(
                client,
                webhook.stream_id,
                webhook.event.data.commit.object_id,
                self._result_branch,
            )

        if branch_name == self._result_branch:
            # slack notifications
            return bots.SlackCarbonNotifier(
                client,
                webhook.stream_id,
                webhook.event.data.id,
                self._slack_token,
                self._slack_channel_id,
                self._report_url,
            )
