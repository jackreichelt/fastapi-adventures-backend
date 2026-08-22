from typing import Annotated

from fastapi import APIRouter, Query

from ..db import get_db
from ..websockets.pubsub import get_pubsub_service

router = APIRouter(
    prefix="/connections",
    tags=["connections"],
)


@router.get("/negotiate")
async def get_slide(
    db: get_db,
    pubsub_service: get_pubsub_service,
    mode: Annotated[str, Query()] = "audience",
):
    pass
    #     let token = await serviceClient.getClientAccessToken({roles: ["webpubsub.joinLeaveGroup", "webpubsub.sendToGroup"] });
    # res.json({
    #     url: token.url
    # });

    token = pubsub_service.get_client_access_token(roles=[mode])
    return token


@router.post("/test")
async def test_receive_message(
    hub: Annotated[str, Query()],
    event: Annotated[str, Query()],
):
    print(f"Event received in {hub}:")
    print(event)
