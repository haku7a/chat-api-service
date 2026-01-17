from sqlmodel import Field, SQLModel
from app.models.types import BodyStr
from datetime import datetime


class MessageBase(SQLModel):
    text: BodyStr


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
