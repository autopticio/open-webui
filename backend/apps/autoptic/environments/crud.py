import logging
import aiohttp

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/read_environment")
async def read_environment(serverUrl: str, endpoint_id: str , env_id: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{serverUrl}story/ep/{endpoint_id}/env/{env_id}",
            )
            data = await response.json()

            return data

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")

@router.get("/get_list_env")
async def getListEnv(endpoint_id: str , serverUrl: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{serverUrl}story/ep/{endpoint_id}/env",
            )
            items = await response.json()

            return items

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")