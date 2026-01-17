from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(title="Chat Application API")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}
