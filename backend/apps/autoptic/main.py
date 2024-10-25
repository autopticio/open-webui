import aiohttp
import re
import logging

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

from .keys import router as keys_router
from .serverconfig import router as serverconfig
from .tokens.crud import router as tokens_router
from .snapshots.crud import router as snapshots_router
from .pql.crud import router as pql_router


from config import (
    ENV
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    docs_url="/docs" if ENV == "dev" else None, redoc_url=None, lifespan=lifespan
)

app.include_router(keys_router, prefix="/keys", tags=["autoptic_keys"])
app.include_router(serverconfig, prefix="/serverconfig", tags=["serverconfig_keys"])
app.include_router(snapshots_router, prefix="/snapshots", tags=["snapshots"])
app.include_router(pql_router, prefix="/pqls", tags=["pqls"])
app.include_router(tokens_router, prefix="/tokens", tags=["token"])

origins = ["*"]

class PQLquery(BaseModel):
    vars: str
    pql: str

class PayloadQuery(BaseModel):
    query: PQLquery
    endpoint: str

# Maybe we can use something like this to check is the EP is correctly written in the config before save,
# but there is a few things to talk about that part of the UI/UX

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
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")



