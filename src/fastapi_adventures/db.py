import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    """
    The base SQLAlchemy class.
    Has an id so that we don't have to specify that on each model.
    """

    id: Mapped[int] = mapped_column(primary_key=True)


if not all(
    [
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_DATABASE"),
        os.getenv("POSTGRES_USERNAME"),
        os.getenv("POSTGRES_PASSWORD"),
        os.getenv("POSTGRES_PORT"),
    ]
):
    raise ValueError("Missing required database environment variables")

DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}"
    "?sslmode=require&channel_binding=require"
)

engine = create_engine(DATABASE_URL)

session_maker = sessionmaker(engine)


async def _get_db():
    """
    Yields a session. Sessions are a transactional connection to the database.
    """
    with session_maker() as session:
        yield session


get_db = Annotated[Session, Depends(_get_db)]
