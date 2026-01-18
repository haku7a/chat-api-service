from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.deps import get_async_session
from app.schemas import ChatRead, ChatCreate
from app.models import Chat

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
