from pydantic import BaseModel
from sqlalchemy.orm import Mapped

from ..db import Base


class Slide(Base):
    __tablename__ = "slides"

    # Direct Attributes
    title: Mapped[str]
    contents: Mapped[str]  # json list of bullet points for slides
    image: Mapped[str]  # image URL
    poll_options: Mapped[str]  # json format: [{option: str, destination: int (slide id)}]


class PublicSlide(BaseModel):
    """
    Pydantic interface for outputting a Slide.
    """

    id: int
    title: str
    contents: str
    image: str
    poll_options: str


class CreateSlide(BaseModel):
    """
    Pydantic interface for creating a Slide.
    """

    title: str
    contents: list[str]
    image: str = ""
    poll_options: list[dict[str, int | str]]
