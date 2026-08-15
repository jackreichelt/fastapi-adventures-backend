from typing import Annotated

from fastapi import APIRouter, Body
from sqlalchemy import delete, select

from ..db import get_db
from ..models.vote import CreateVote, GetVote, PublicVote, Vote
from ..websockets.connection_manager import get_presenter_connections

router = APIRouter(
    prefix="/votes",
    tags=["voting"],
)


@router.get("/{session_id}/{slide_id}", response_model=list[PublicVote])
async def get_votes(
    db: get_db,
    session_id: int,
    slide_id: int,
):
    """
    Fetches all the votes for a given session on a given slide.
    """
    stmt = select(Vote).where(Vote.session_id == session_id).where(Vote.slide_id == slide_id)
    votes = db.scalars(stmt).all()

    return [PublicVote.model_validate(v, from_attributes=True) for v in votes]


@router.post("/fetch", response_model=PublicVote | None)
async def get_vote(
    db: get_db,
    vote_data: Annotated[GetVote, Body()],
):
    """
    Fetches a user's vote, if it exists.
    """
    stmt = (
        select(Vote)
        .where(Vote.audience_id == vote_data.audience_id)
        .where(Vote.slide_id == vote_data.slide_id)
        .where(Vote.session_id == vote_data.session_id)
    )
    existing_vote = db.scalar(stmt)

    if existing_vote:
        PublicVote.model_validate(existing_vote, from_attributes=True)

    return None


@router.post("", response_model=PublicVote)
async def vote(
    db: get_db,
    presenter_connections: get_presenter_connections,
    vote_data: Annotated[CreateVote, Body()],
):
    """
    Creates a new slide
    """
    stmt = (
        select(Vote)
        .where(Vote.audience_id == vote_data.audience_id)
        .where(Vote.slide_id == vote_data.slide_id)
        .where(Vote.session_id == vote_data.session_id)
    )
    old_vote = db.scalar(stmt)

    if old_vote:
        stmt = delete(Vote).where(Vote.id == old_vote.id)
        db.execute(stmt)
        await presenter_connections.broadcast(f"Vote removed: {old_vote.audience_id} for {old_vote.option_id}")

    new_vote = Vote(
        audience_id=vote_data.audience_id,
        option_id=vote_data.option_id,
        slide_id=vote_data.slide_id,
        session_id=vote_data.session_id,
    )
    db.add(new_vote)
    db.commit()

    await presenter_connections.broadcast(f"Vote added: {new_vote.audience_id} for {new_vote.option_id}")

    return PublicVote.model_validate(new_vote, from_attributes=True)
