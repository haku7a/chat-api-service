import pytest
from app.models.chat import Chat
from app.models.message import Message
from sqlmodel import select
from sqlalchemy.orm import selectinload


async def test_relationship_cascade(db_session):
    chat = Chat(title="Test Chat")
    message1 = Message(text="Hello", chat=chat)
    message2 = Message(text="World", chat=chat)

    db_session.add(chat)
    await db_session.commit()

    chat_id = chat.id

    result = await db_session.exec(select(Message).where(Message.chat_id == chat_id))
    messages = result.all()
    assert len(messages) == 2

    await db_session.delete(chat)
    await db_session.commit()

    result = await db_session.exec(select(Message).where(Message.chat_id == chat_id))
    messages = result.all()
    assert len(messages) == 0


async def test_get_chat_with_messages(db_session):
    chat = Chat(title="Chat with Messages")
    message1 = Message(text="First Message", chat=chat)
    message2 = Message(text="Second Message", chat=chat)

    db_session.add(chat)
    await db_session.commit()

    result = await db_session.exec(
        select(Chat).where(Chat.id == chat.id).options(selectinload(Chat.messages))
    )
    fetched_chat = result.one()
    assert len(fetched_chat.messages) == 2
