import logging
import aiohttp
import os

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

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

@router.get("/read_snapshot")
async def readSnapshot(endpoint_id: str, pql_id: str, format: str, timestamp: str, snapshot_id: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}",
            )
            
            html_content = await response.text()

            return HTMLResponse(content=html_content)

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")

# This is not working. WHY is not working?    
@router.delete("/delete_snapshot")
async def deleteSnapshots(endpoint_id: str, pql_id: str, format: str, timestamp: str, snapshot_id: str):
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.delete(
                f"http://localhost:9999/story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}",
            )
            
            if response.status == 200:
                return '', 204

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    