from typing import Annotated

from fastapi import APIRouter, Body, Query

from ..db import get_db
from ..models.pubsub_event import PubsubEvent
from ..websockets.pubsub import get_pubsub_service

router = APIRouter(
    prefix="/connections",
    tags=["connections"],
)


@router.get("/negotiate")
async def get_slide(
    pubsub_service: get_pubsub_service,
    audience_id: Annotated[str, Query()],
    mode: Annotated[str, Query()] = "audience",
):
    token = pubsub_service.get_client_access_token(
        user_id=audience_id,
        groups=[mode],
        roles=["webpubsub.sendToGroup", "webpubsub.joinLeaveGroup"],
    )
    return token


@router.post("/test")
async def test_receive_message(
    db: get_db,
    event: Annotated[str, Body()],
):
    print("Event received:")
    print(event)

    new_event = PubsubEvent(hub="hub", event=event)
    db.add(new_event)
    db.commit()
