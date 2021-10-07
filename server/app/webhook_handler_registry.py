from dataclasses import dataclass
from typing import Callable, Dict, Optional

from specklepy.api.client import SpeckleClient
from speckle_calculator.service import carbon, discord

from app.models import Webhook


@dataclass
class WebhookHandlerRegistry:

    _token_registry: Dict[str, str]
    _discord_url: str
    _report_url: str
    _tracked_branch: str = "main"
    _result_branch: str = "carbon-results"

    def __call__(self, webhook: Webhook) -> Optional[Callable[[None], None]]:
        branch_name = webhook.event.data.commit.branch_name
        server_url = webhook.server.canonical_url
        if token := self._token_registry.get(server_url):
            client = SpeckleClient(
                host=webhook.server.canonical_url,
                use_ssl=server_url.startswith("https://"),
            )
            client.authenticate(token)
        else:
            raise ValueError(f"The application is not autorized on {server_url} server")

        if branch_name == self._tracked_branch:
            return carbon.CarbonCalculator(
                client,
                webhook.stream_id,
                webhook.event.data.commit.object_id,
                self._result_branch,
            )

        elif branch_name == self._result_branch:
            discord_url = ""
            report_url = ""
            return discord.DiscordCarbonNotifier(
                client,
                webhook.stream_id,
                self._tracked_branch,
                self._discord_url,
                self._report_url,
            )
