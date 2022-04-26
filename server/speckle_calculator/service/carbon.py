from dataclasses import dataclass

from speckle_calculator import core

from specklepy.api.operations import receive, send
from specklepy.transports.server import ServerTransport
from specklepy.api.client import SpeckleClient


@dataclass
class CarbonCalculator:
    client: SpeckleClient
    stream_id: str
    input_object_id: str
    target_branch_name: str = "carbon-results"

    def __call__(self) -> None:
        """
        Create carbon report data for speckle commit.

        Steps:
            * get commit data from server
            * call domain function
            * make sure the new branch exists
            * push result to a separate branch
        """
        transport = ServerTransport(self.stream_id, self.client)
        input_base = receive(self.input_object_id, transport)
        result = core.calculate_carbon(input_base)

        self.client.branch.create(self.stream_id, self.target_branch_name)
        sent_id = send(result, [transport])

        self.client.commit.create(
            self.stream_id,
            sent_id,
            self.target_branch_name,
        )
