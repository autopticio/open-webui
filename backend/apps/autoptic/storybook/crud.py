import logging
import aiohttp
import os

from fastapi import APIRouter
from fastapi import HTTPException

# autoptic_port=os.getenv('AUTOPTIC_SERVER_PORT')

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post("/save_env")
async def createToken(endpoint_id=1,pql_id=1):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}",
            )
            assert response.status == 201
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.get("/read_env")
async def createToken(endpoint_id=1,pql_id=1):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}",
            )
            assert response.status == 201
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.delete("/delete_env")
async def createToken(endpoint_id=1,pql_id=1):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}",
            )
            assert response.status == 201
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    
@router.get("/read_env_list")
async def createToken(endpoint_id=1):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.post(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql",
            )
            assert response.status == 201
            text = await response.text()
            return text
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")