import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_async_session
from app.models import Chat, Message
from app.schemas import MessageCreate, MessageRead

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message_in: MessageCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Message:
    db_chat = await db.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    db_message = Message.model_validate(message_in, update={"chat_id": chat_id})

    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    logger.info(f"New message added to chat {chat_id}")
    return db_message
