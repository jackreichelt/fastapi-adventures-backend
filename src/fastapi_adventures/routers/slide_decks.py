from typing import Annotated

from fastapi import APIRouter, Body
from sqlalchemy import select

from ..db import get_db
from ..models.slide_deck import CreateSlideDeck, PublicSlideDeck, SlideDeck

router = APIRouter(
    prefix="/slide-decks",
    tags=["slide-decks"],
)


@router.get("", response_model=list[PublicSlideDeck])
async def get_slide_decks(
    db: get_db,
) -> list[PublicSlideDeck]:
    """
    Gets all slide decks
    """
    stmt = select(SlideDeck)
    slide_decks = db.scalars(stmt).all()

    return [PublicSlideDeck.model_validate(slide_deck, from_attributes=True) for slide_deck in slide_decks]


@router.post("", response_model=PublicSlideDeck)
async def add_slide_deck(
    db: get_db,
    deck_data: Annotated[CreateSlideDeck, Body()],
):
    """
    Creates a new slide
    """
    new_slide_deck = SlideDeck(
        title=deck_data.title,
        first_slide_id=deck_data.first_slide_id,
    )

    db.add(new_slide_deck)
    db.commit()

    return PublicSlideDeck.model_validate(new_slide_deck, from_attributes=True)
