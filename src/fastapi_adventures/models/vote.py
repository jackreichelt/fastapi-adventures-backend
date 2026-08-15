from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .presentation_session import PresentationSession, PublicPresentationSession
from .slide import PublicSlide, Slide


class Vote(Base):
    __tablename__ = "votes"

    # Direct Attributes
    audience_id: Mapped[str]
    option_id: Mapped[int]

    # Relationships
    slide_id: Mapped[int] = mapped_column(ForeignKey("slides.id"))
    slide: Mapped["Slide"] = relationship()
    session_id: Mapped[int] = mapped_column(ForeignKey("presentation_sessions.id"))
    session: Mapped["PresentationSession"] = relationship()


class PublicVote(BaseModel):
    """
    Pydantic interface for outputting a Slide.
    """

    id: int
    audience_id: str
    option_id: int
    slide: "PublicSlide"
    session: "PublicPresentationSession"


class CreateVote(BaseModel):
    """
    Pydantic interface for creating a Vote.
    """

    audience_id: str
    option_id: int
    slide_id: int
    session_id: int


class GetVote(BaseModel):
    """
    Pydantic interface for fetching an audience member's Vote.
    """

    audience_id: str
    slide_id: int
    session_id: int
