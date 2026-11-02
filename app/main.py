import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.config import Settings, get_settings
from app.llm import ask_gemini

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="CacheCompass", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


class AskRequest(BaseModel):
    question: str


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Check whether the application is running."""
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/ask")
def ask(request: AskRequest) -> dict:
    """Send a question to Gemini and return its answer."""
    try:
        answer = ask_gemini(request.question)

        return {
            "question": request.question,
            "answer": answer,
        }

    except Exception:
        logger.exception("Exception occurred while processing /ask:")
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again later.",
        )