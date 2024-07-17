import aiohttp
import re
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from .keys import router as keys_router

from config import (
    ENV
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(
    docs_url="/docs" if ENV == "dev" else None, redoc_url=None, lifespan=lifespan
)

app.include_router(keys_router, prefix="/keys", tags=["autoptic_keys"])

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
        print(f"Invalid keys for Autoptic. Error: {str(e)}")
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")
