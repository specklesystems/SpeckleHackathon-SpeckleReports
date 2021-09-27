import os

async def speckle_token_provider() -> str:
    return os.environ["SPECKLE_TOKEN"]
