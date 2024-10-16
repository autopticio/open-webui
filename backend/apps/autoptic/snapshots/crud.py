import logging
import aiohttp
import os

from fastapi import APIRouter
from fastapi import HTTPException

# autoptic_port=os.getenv('AUTOPTIC_SERVER_PORT')

router = APIRouter()

logger = logging.getLogger(__name__)

def transform_snapshot_to_dict(path):
    segments = path.split('/')
    
    snapshot = { 
                 'url': path,
                 'endpoint_id': segments[2],
                 'pql_id': segments[4],
                 'format': segments[6],
                 'timestamp': segments[7],
                 'snapshot_id': segments[8]}
    
    return snapshot

@router.get("/get_list_snapshot")
async def getListSnapshots(endpoint_id: str, pql_id: str, format: str, timestamp: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}",
            )
            response = await response.json()

            list_snapshots = []
            if not response:
                return list_snapshots

            for snap in response:
                list_snapshots.append(transform_snapshot_to_dict(snap))
            return list_snapshots
        
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")