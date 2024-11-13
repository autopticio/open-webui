import logging
import aiohttp
import re

from fastapi import Depends, APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from apps.webui.models.users import Users

from utils.utils import (
    get_current_user,
)

router = APIRouter()

logger = logging.getLogger(__name__)


############################
# Autoptic Keys
############################

class AutopticEnvironment(BaseModel):
    autoptic_environment: str
    envFileName: str

# Server URL

@router.post("/healthcheck")
async def healthcheck(serverURL: dict, user=Depends(get_current_user)):
    server_url = serverURL["serverURL"]
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            response = await session.get(
                f"{server_url}health"
            )
            if response.status == 200:
                return True
            else:
                raise HTTPException(status_code=response.status, detail=f"Server returned status code {response.status}")
    except Exception as e:
        logger.error(" Failed to update server URL. %s", e)
        raise HTTPException(status_code=500, detail="Failed to update server URL. Database error.")


@router.post("/new_serverURL")
async def update_serverURL(serverURL: dict, user=Depends(get_current_user)):
    server_url = serverURL["serverURL"]
    try:
        success = Users.update_user_serverURL_by_id(user.id, serverURL["serverURL"])
        if success:
            return {
                "serverURL": server_url,
            }
    except Exception as e:
        logger.error(" Failed to update server URL. %s", e)
        raise HTTPException(status_code=500, detail="Failed to update server URL. Database error.")
    
@router.get("/get_serverURL")
async def get_serverURL(user=Depends(get_current_user)):
    try:
        serverURL = Users.get_user_serverURL_by_id(user.id)
        if serverURL:
            return {
                "serverURL": serverURL,
            }
        return {
                "serverURL": '',
            }
    except Exception as e:
        logger.error(" Failed to get server URL. %s", e)
        raise HTTPException(status_code=500, detail="Failed to get server URL. Database error.")

@router.delete("/delete_serverURL")
async def delete_serverURL(user=Depends(get_current_user)):
    success = Users.update_user_serverURL_by_id(user.id, None)
    return success

# Endpoint

@router.post("/new_endpointID")
async def update_autoptic_endpoint(endpointID: dict, user=Depends(get_current_user)):
    try:
        success = Users.update_user_endpointID_by_id(user.id, endpointID["endpointID"])
        if success:
            return {
                "endpointID": endpointID["endpointID"],
            }
    except Exception as e:
        logger.error(" Failed to update endpoint ID. %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to update endpoint ID. Database error.")
    
@router.get("/get_endpointID")
async def get_endpointID(user=Depends(get_current_user)):
    try:
        endpointID = Users.get_user_endpointID_by_id(user.id)
        if endpointID:
            return {
                "endpointID": endpointID,
            }
        return {
            "endpointID": '',
        }
    except Exception as e:
        logger.error(" Failed to get Autoptic endpoint. %s", e)
        raise HTTPException(status_code=500, detail="Failed to get endpoint ID. Database error.")

@router.delete("/delete_endpointID")
async def delete_endpointID(user=Depends(get_current_user)):
    success = Users.update_user_endpointID_by_id(user.id, None)
    return success