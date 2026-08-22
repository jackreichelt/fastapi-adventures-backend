import os
from typing import Annotated

from azure.messaging.webpubsubservice import WebPubSubServiceClient
from fastapi import Depends

CONNECTION_STRING = os.getenv("PUBSUB_CONNECTION_STRING", "")
service = WebPubSubServiceClient.from_connection_string(connection_string=CONNECTION_STRING, hub="hub")


async def yield_pubsub_service():
    """
    Yields the Azure Web PubSub Service client.
    """
    yield service


get_pubsub_service = Annotated[WebPubSubServiceClient, Depends(yield_pubsub_service)]
