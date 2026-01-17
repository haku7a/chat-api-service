from sqlmodel import SQLModel, Field
from app.models.types import TitleStr
from datetime import datetime

from app.schemas.message import MessageRead


class ChatBase(SQLModel):
    title: TitleStr = Field(max_length=200)


class ChatCreate(ChatBase):
    pass


class ChatRead(ChatBase):
    id: int
    created_at: datetime


class ChatWithMessages(ChatRead):
    messages: list[MessageRead] = []
