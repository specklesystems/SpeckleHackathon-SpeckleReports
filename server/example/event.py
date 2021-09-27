from app.main import Webhook, CommitCreateEvent
from pathlib import Path
from devtools import debug

if __name__ == "__main__":

    debug(Webhook.parse_raw(Path("example/event.json").read_text()))