import uuid
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, Query, status
from sqlalchemy import select

from ..db import get_db
from ..models.presentation_session import (
    CreatePresentationSession,
    PresentationSession,
    PublicAudiencePresentationSession,
    PublicPresentationSession,
)

router = APIRouter(
    prefix="/presentation-session",
    tags=["presenting"],
)


@router.post("", response_model=PublicPresentationSession)
async def start_presentation_session(
    db: get_db,
    presentation_session_data: Annotated[CreatePresentationSession, Body()],
):
    """
    Creates a new presentation session as the host
    """
    print("presentation_session_data", presentation_session_data)
    new_presentation_session = PresentationSession(
        current_slide_id=presentation_session_data.first_slide_id,
        attendees=0,
    )
    db.add(new_presentation_session)
    db.commit()

    return PublicPresentationSession.model_validate(new_presentation_session, from_attributes=True)


@router.get("/{session_id}", response_model=PublicPresentationSession)
async def resume_presentation_session(
    db: get_db,
    session_id: Annotated[int, Path()],
):
    """
    Resumes a presentation session as the host
    """
    stmt = select(PresentationSession).where(PresentationSession.id == session_id)
    presentation_session = db.scalar(stmt)

    return PublicPresentationSession.model_validate(presentation_session, from_attributes=True)


@router.get("/join/{session_id}", response_model=PublicAudiencePresentationSession)
async def join_presentation_session(
    db: get_db,
    session_id: Annotated[int, Path()],
    audience_id: Annotated[str, Query()] = "",
):
    """
    Joins a presentation session as an audience member
    """
    stmt = select(PresentationSession).where(PresentationSession.id == session_id)
    presentation_session = db.scalar(stmt)

    if presentation_session:
        presentation_session.attendees += 1
        db.commit()

        AudienceSession = PublicAudiencePresentationSession.model_validate(presentation_session, from_attributes=True)
        if audience_id:
            AudienceSession.audience_id = audience_id
        else:
            AudienceSession.audience_id = str(uuid.uuid4())
        return AudienceSession
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Presentation session not found")


@router.get(
    "/join/{session_id}/{audience_id}",
    response_model=PublicAudiencePresentationSession,
)
async def rejoin_presentation_session(
    db: get_db,
    session_id: Annotated[int, Path()],
    audience_id: Annotated[str, Path()],
):
    """
    Rejoins a presentation session as an audience member
    """
    stmt = select(PresentationSession).where(PresentationSession.id == session_id)
    presentation_session = db.scalar(stmt)

    if presentation_session:
        response = PublicAudiencePresentationSession.model_validate(
            presentation_session,
            from_attributes=True,
        )
        response.audience_id = audience_id
        return response
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Presentation session not found")
