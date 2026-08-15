from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .slide import PublicSlide, Slide

if TYPE_CHECKING:  # pragma: no cover
    pass


class SlideDeck(Base):
    __tablename__ = "slide_decks"

    title: Mapped[str]

    # Relationships
    first_slide_id: Mapped[int] = mapped_column(ForeignKey("slides.id"))
    first_slide: Mapped["Slide"] = relationship()


class PublicSlideDeck(BaseModel):
    """
    Pydantic interface for outputting a Session.
    """

    id: int
    title: str
    first_slide_id: int
    first_slide: PublicSlide


class CreateSlideDeck(BaseModel):
    """
    Pydantic interface for creating a Session.
    """

    title: str
    first_slide_id: int
