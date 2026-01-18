import logging
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.endpoints.chats import router as chats_router
from app.api.endpoints.messages import router as messages_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Chat Application API")

app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(
    messages_router, prefix="/chats/{chat_id}/messages", tags=["messages"]
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}
