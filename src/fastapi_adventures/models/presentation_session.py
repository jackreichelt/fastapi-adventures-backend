from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .slide import PublicSlide, Slide

if TYPE_CHECKING:  # pragma: no cover
    pass


class PresentationSession(Base):
    __tablename__ = "presentation_sessions"

    # Direct Attributes
    attendees: Mapped[int] = mapped_column(default=0, server_default="0")

    # Relationships
    current_slide_id: Mapped[int] = mapped_column(ForeignKey("slides.id"))
    current_slide: Mapped["Slide"] = relationship()


class PublicPresentationSession(BaseModel):
    """
    Pydantic interface for outputting a Session.
    """

    id: int
    attendees: int
    current_slide_id: int
    current_slide: PublicSlide


class PublicAudiencePresentationSession(BaseModel):
    """
    Pydantic interface for outputting a Session.
    """

    id: int
    audience_id: str = ""
    current_slide_id: int
    current_slide: PublicSlide


class CreatePresentationSession(BaseModel):
    """
    Pydantic interface for creating a Session.
    """

    first_slide_id: int = 1
