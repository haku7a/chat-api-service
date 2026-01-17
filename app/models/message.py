from typing import TYPE_CHECKING
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from .types import BodyStr

if TYPE_CHECKING:
    from .chat import Chat


class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: BodyStr = Field(index=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    chat_id: int = Field(foreign_key="chat.id", index=True)
    chat: Optional["Chat"] = Relationship(back_populates="messages")

    model_config = {"validate_assignment": True}
