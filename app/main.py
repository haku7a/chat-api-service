from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.endpoints.chats import router as chats_router


app = FastAPI(title="Chat Application API")

app.include_router(chats_router, prefix="/chats", tags=["chats"])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}
