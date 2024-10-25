import logging

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

@router.post("/new_serverURL")
async def update_serverURL(serverURL: dict, user=Depends(get_current_user)):
    try:
        print(serverURL)
        success = Users.update_user_serverURL_by_id(user.id, serverURL["serverURL"])
        print(success)
        if success:
            return {
                "serverURL": serverURL["serverURL"],
            }
    except Exception as e:
        logger.error(" Failed to update server URL. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to update server URL. Error: {str(e)}")
    
@router.get("/get_serverURL")
async def get_serverURL(user=Depends(get_current_user)):
    try:
        serverURL = Users.get_user_serverURL_by_id(user.id)
        if serverURL:
            return {
                "serverURL": serverURL,
            }
    except Exception as e:
        logger.error(" Failed to get server URL. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to get server URL. Error: {str(e)}")

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
        raise HTTPException(status_code=404, detail=f"Failed to update endpoint ID. Error: {str(e)}")
    
@router.get("/get_endpointID")
async def get_endpointID(user=Depends(get_current_user)):
    try:
        endpointID = Users.get_user_endpointID_by_id(user.id)
        if endpointID:
            return {
                "endpointID": endpointID,
            }
    except Exception as e:
        logger.error(" Failed to get Autoptic endpoint. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to get endpoint ID. Error: {str(e)}")

@router.delete("/delete_endpointID")
async def delete_endpointID(user=Depends(get_current_user)):
    success = Users.update_user_endpointID_by_id(user.id, None)
    return success