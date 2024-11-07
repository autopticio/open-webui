import logging
import aiohttp
import os
import json

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/get_list_pql")
async def getListPQL(endpoint_id: str , serverURL: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{serverURL}story/ep/{endpoint_id}/pql",
            )

            return await response.json()

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=403, detail="Invalid keys for Autoptic.")
    
    