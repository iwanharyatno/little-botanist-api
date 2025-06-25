from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Gemini Proxy API",
    description="API Proxy untuk interaksi dengan Google Gemini Vision",
    version="1.0"
)

app.include_router(router)
