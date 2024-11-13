import logging
import aiohttp
import os
import concurrent.futures

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from ..pql.crud import getListPQL
from datetime import datetime

# autoptic_port=os.getenv('AUTOPTIC_SERVER_PORT')


def split_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def execute_transformation(path_list,num_threads=500):

    snapshots_dicts = []
    path_sub_list = list(split_list(path_list, len(path_list) // num_threads + 1))

    # Create a ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:

        futures = [executor.submit(transform_snapshot_to_dict, path_sublist) for path_sublist in path_sub_list]
        # Optionally, wait for all futures to complete and handle any exceptions
        for future in concurrent.futures.as_completed(futures):
            snapshots_dicts.extend(future.result())

    return snapshots_dicts

router = APIRouter()

logger = logging.getLogger(__name__)

def transform_snapshot_to_dict(path_list):
    snapshot_in_dict_list=[]
    for path in path_list:
        segments = path.split('/')

        snapshot = { 
                    'url': path,
                    'endpoint_id': segments[2],
                    'pql_id': segments[4],
                    'format': segments[6],
                    'timestamp': segments[7],
                    'snapshot_id': segments[8]}

        snapshot_in_dict_list.append(snapshot)

    return snapshot_in_dict_list

formats = ['html','json']

@router.get("/get_default_list_snapshot")
async def getDefaultListSnapshots(endpoint_id: str, window: str, serverURL: str):

    list_snapshots = []
    pql_ids = await getListPQL(endpoint_id, serverURL)

    for pql_id in pql_ids:
        for format in formats:

            try:
                async with aiohttp.ClientSession(trust_env=True) as session:
                    response = await session.post(
                        f"{serverURL}story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/recent?window={window}",
                    )
                    response = await response.json()
                    if response:
                        list_snapshots.extend(execute_transformation(response))                

            except Exception as e:
                raise HTTPException(status_code=500, detail="something went wrong.")

        return list_snapshots

@router.get("/get_list_snapshot")
async def getListSnapshots(endpoint_id: str, pql_id: str, format: str, timestamp: str, serverURL: str):
    
    list_snapshots = []
    
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{serverURL}story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}",
            )
            response = await response.json()

            if response:
                list_snapshots.extend(response)

        list_snapshots = execute_transformation(list_snapshots)

        return list_snapshots
        
    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")

@router.get("/read_snapshot")
async def readSnapshot(endpoint_id: str, pql_id: str, format: str, timestamp: str, snapshot_id: str, serverURL: str):
    
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{serverURL}story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}",
            )
            
            html_content = await response.text()

            return HTMLResponse(content=html_content)

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")

@router.delete("/delete_snapshot")
async def deleteSnapshots(endpoint_id: str, pql_id: str, format: str, timestamp: str, snapshot_id: str, serverURL: str):
    
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.delete(
                f"{serverURL}story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}",
            )
            
            if response.status == 200:
                return True

    except Exception as e:
        logger.error(" Invalid keys for Autoptic. %s", e)
        raise HTTPException(status_code=500, detail="something went wrong.")
    