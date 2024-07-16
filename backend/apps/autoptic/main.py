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
    ENV
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    docs_url="/docs" if ENV == "dev" else None, redoc_url=None, lifespan=lifespan
)

origins = ["*"]

class PQLquery(BaseModel):
    vars: str
    pql: str

class PayloadQuery(BaseModel):
    query: PQLquery
    endpoint: str

@app.post("/runPQL")    
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