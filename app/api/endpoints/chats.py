from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.api.deps import get_async_session
from app.schemas import ChatRead, ChatCreate, ChatWithMessages
from app.models import Chat, Message

router = APIRouter()


@router.post("/", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_in: ChatCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Chat:
    db_chat = Chat.model_validate(chat_in)
    db.add(db_chat)
    await db.commit()
    await db.refresh(db_chat)
    return db_chat


@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_async_session),
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> Chat:
    db_chat = await db.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    statement = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
    )
    result = await db.exec(statement)
    messages = result.all()

    return {
        "id": db_chat.id,
        "title": db_chat.title,
        "created_at": db_chat.created_at,
        "messages": list(reversed(messages)),
    }


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    db_chat = await db.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    await db.delete(db_chat)
    await db.commit()
    return None
