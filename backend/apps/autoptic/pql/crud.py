import logging
import aiohttp
import os
import json

from fastapi import APIRouter
from fastapi import HTTPException

# autoptic_port=os.getenv('AUTOPTIC_SERVER_PORT')

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/get_list_pql")
async def getListPQL(endpoint_id: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql",
            )

            return await response.json()

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")
    
    