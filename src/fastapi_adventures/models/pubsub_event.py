from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped

from ..db import Base

if TYPE_CHECKING:  # pragma: no cover
    pass


class PubsubEvent(Base):
    __tablename__ = "pubsub_events"

    # Direct Attributes
    hub: Mapped[str]
    event: Mapped[str]
