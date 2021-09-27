from dataclasses import dataclass

from speckle_carbon import core

from specklepy.api.operations import receive, send
from specklepy.transports.abstract_transport import AbstractTransport
from specklepy.transports.server import ServerTransport
from specklepy.api.client import SpeckleClient


@dataclass
class CarbonInput:
    """Input datastructure for carbon calculation."""

    stream_id: str
    object_id: str
    target_branch_name: str = "carbon-results"


async def calculate_carbon(
    carbon_input: CarbonInput, transport: AbstractTransport, client: SpeckleClient
):
    """
    Create carbon report data for speckle commit.

    Steps:
        * get commit data from server
        * call domain function
        * make sure the new branch exists
        * push result to a separate branch
    """

    input_base = receive(carbon_input.object_id, transport)

    client.branch.create(
        carbon_input.stream_id, carbon_input.target_branch_name
    )

    result = core.calculate_carbon(input_base)

    sent_id = send(result, [transport])

    client.commit.create(
        carbon_input.stream_id,
        sent_id,
        carbon_input.target_branch_name,
    )
