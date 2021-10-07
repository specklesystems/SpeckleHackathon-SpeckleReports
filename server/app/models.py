from pydantic import BaseModel
import stringcase


class CarbonBase(BaseModel):
    """Carbon base model"""

    class Config:
        # enables auto convert to and from camelcase json
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
