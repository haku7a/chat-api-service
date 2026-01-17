from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .types import TitleStr
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .message import Message


class Chat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: TitleStr = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )

    messages: list["Message"] = Relationship(
        back_populates="chat", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    model_config = {"validate_assignment": True}
