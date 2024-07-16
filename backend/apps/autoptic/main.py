import aiohttp
import re
from fastapi import FastAPI, Request, Depends, APIRouter
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

from apps.webui.models.users import Users

from utils.utils import (
    get_current_user,
)

from config import (
    ENV
)

router = APIRouter()

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


def extract_id_from_url(url: str) -> str:
    pattern = r'^(?:(https?://)?autoptic\.io/pql/ep/([a-zA-Z0-9-]+)/run|([a-zA-Z0-9-]+))$'
    match = re.match(pattern, url)
    if match:
        if match.group(2):
            return match.group(2)  # String capturado entre "ep/" y "/run"
        elif match.group(3):
            return match.group(3)  # String que no coincide con el patrón de URL completo
    return "None"

@app.post("/runPQL")
async def sentToAutoptic(Payload: PayloadQuery):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            endpoint_id = extract_id_from_url(Payload.endpoint)
            response = await session.post(
                f"https://autoptic.io/pql/ep/{endpoint_id}/run",
                json=Payload.query.dict()
            )
            assert response.status == 200
            text = await response.text()
            return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# delete autoptic variables
@router.delete("/delete_autoptic_environment")
async def delete_autoptic_environment(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_environment_by_id(user.id, None,None)
    return success