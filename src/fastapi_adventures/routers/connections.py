from typing import Annotated

from fastapi import APIRouter, Query

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
    token = pubsub_service.get_client_access_token(user_id=audience_id, roles=[mode])
    return token


@router.post("/test")
async def test_receive_message(
    hub: Annotated[str, Query()],
    event: Annotated[str, Query()],
):
    print(f"Event received in {hub}:")
    print(event)
