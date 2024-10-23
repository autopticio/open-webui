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

#update autoptic endpoint
@router.post("/new_serverURL")
async def update_serverURL(autoptic_endpoint: dict, user=Depends(get_current_user)):
    try:
        success = Users.update_user_serverURL_by_id(user.id, autoptic_endpoint["autoptic_endpoint"])
        if success:
            return {
                "autoptic_endpoint": autoptic_endpoint["autoptic_endpoint"],
            }
    except Exception as e:
        logger.error(" Failed to update Autoptic endpoint. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to update Autoptic endpoint. Error: {str(e)}")
    
# get autoptic endpoint
@router.get("/get_autoptic_endpoint")
async def get_autoptic_endpoint(user=Depends(get_current_user)):
    try:
        autoptic_endpoint = Users.get_user_autoptic_endpoint_by_id(user.id)
        if autoptic_endpoint:
            return {
                "autoptic_endpoint": autoptic_endpoint,
            }
    except Exception as e:
        logger.error(" Failed to get Autoptic endpoint. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to get Autoptic endpoint. Error: {str(e)}")

# delete autoptic endpoint
@router.delete("/delete_autoptic_endpoint")
async def delete_autoptic_endpoint(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_endpoint_by_id(user.id, None)
    return success

# Endpoint

#update autoptic endpoint
@router.post("/new_autoptic_endpoint")
async def update_autoptic_endpoint(autoptic_endpoint: dict, user=Depends(get_current_user)):
    try:
        success = Users.update_user_autoptic_endpoint_by_id(user.id, autoptic_endpoint["autoptic_endpoint"])
        if success:
            return {
                "autoptic_endpoint": autoptic_endpoint["autoptic_endpoint"],
            }
    except Exception as e:
        logger.error(" Failed to update Autoptic endpoint. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to update Autoptic endpoint. Error: {str(e)}")
    
# get autoptic endpoint
@router.get("/get_autoptic_endpoint")
async def get_autoptic_endpoint(user=Depends(get_current_user)):
    try:
        autoptic_endpoint = Users.get_user_autoptic_endpoint_by_id(user.id)
        if autoptic_endpoint:
            return {
                "autoptic_endpoint": autoptic_endpoint,
            }
    except Exception as e:
        logger.error(" Failed to get Autoptic endpoint. %s", e)
        raise HTTPException(status_code=404, detail=f"Failed to get Autoptic endpoint. Error: {str(e)}")

# delete autoptic endpoint
@router.delete("/delete_autoptic_endpoint")
async def delete_autoptic_endpoint(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_endpoint_by_id(user.id, None)
    return success