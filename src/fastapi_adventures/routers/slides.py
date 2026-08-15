import json
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Path, status
from sqlalchemy import select

from ..db import get_db
from ..models.slide import CreateSlide, PublicSlide, Slide

router = APIRouter(
    prefix="/slides",
    tags=["slides"],
)


@router.get("/{slide_id}", response_model=PublicSlide)
async def get_slide(
    db: get_db,
    slide_id: Annotated[int, Path()],
) -> PublicSlide:
    """
    Gets a slide
    """
    stmt = select(Slide).where(Slide.id == slide_id)
    slide = db.scalar(stmt)
    if not slide:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Slide not found")

    # TODO: broadcast new slide change message to audience

    return PublicSlide.model_validate(slide, from_attributes=True)


@router.post("", response_model=PublicSlide)
async def add_slide(
    db: get_db,
    slide_data: Annotated[CreateSlide, Body()],
):
    """
    Creates a new slide
    """
    new_slide = Slide(
        title=slide_data.title,
        contents=json.dumps(slide_data.contents),
        image=slide_data.image,
        poll_options=json.dumps(slide_data.poll_options),
    )
    db.add(new_slide)
    db.commit()

    return PublicSlide.model_validate(new_slide, from_attributes=True)
