import aiohttp

from fastapi import FastAPI, Request, Depends, status, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response
from pydantic import BaseModel
from contextlib import asynccontextmanager

from config import (
    SRC_LOG_LEVELS,
    CACHE_DIR,
    UPLOAD_DIR,
    WHISPER_MODEL,
    WHISPER_MODEL_DIR,
    WHISPER_MODEL_AUTO_UPDATE,
    DEVICE_TYPE,
    AUDIO_STT_OPENAI_API_BASE_URL,
    AUDIO_STT_OPENAI_API_KEY,
    AUDIO_TTS_OPENAI_API_BASE_URL,
    AUDIO_TTS_OPENAI_API_KEY,
    AUDIO_STT_ENGINE,
    AUDIO_STT_MODEL,
    AUDIO_TTS_ENGINE,
    AUDIO_TTS_MODEL,
    AUDIO_TTS_VOICE,
    AppConfig,
    ENV
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    docs_url="/docs" if ENV == "dev" else None, redoc_url=None, lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "This is the Autoptic app"}

origins = ["*"]

class PQLquery(BaseModel):
    vars: str
    pql: str

class PayloadQuery(BaseModel):
    query: PQLquery
    endpoint: str

@app.post("/api/runPQL")    
async def sentToAutoptic(Payload: PayloadQuery):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"https://autoptic.io/pql/ep/{Payload.endpoint}/run",
                json=Payload.query.dict()
            )
        assert response.status == 200
        text= await response.text()
        return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))