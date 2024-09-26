import logging
import aiohttp
import os

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import HTTPException

class Payload(BaseModel):
    endpoint_id: str
    token_id: str

autoptic_port=os.getenv('AUTOPTIC_SERVER_PORT')

url='http://localhost:9999'

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/create_token")
async def createToken(credentials: Payload):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"{url}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
            )
            assert response.status == 201
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.get("/read_token")
async def createToken(credentials: Payload):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"{url}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
            )
            assert response.status == 200
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.delete("/delete_token")
async def createToken(credentials: Payload):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"{url}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
            )
            assert response.status == 200
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.get("/read_token_list")
async def createToken(credentials: Payload):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"{url}/story/ep/{credentials.endpoint_id}/token",
            )
            assert response.status == 200
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")