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
        raise HTTPException(status_code=500, detail="Failed to update Autoptic endpoint. Database error.")
    
# get autoptic endpoint
@router.get("/get_autoptic_endpoint")
async def get_autoptic_endpoint(user=Depends(get_current_user)):
    try:
        autoptic_endpoint = Users.get_user_autoptic_endpoint_by_id(user.id)
        if autoptic_endpoint:
            return {
                "autoptic_endpoint": autoptic_endpoint,
            }
        return {
            "autoptic_endpoint": '',
        }
    except Exception as e:
        logger.error(" Failed to get Autoptic endpoint. %s", e)
        raise HTTPException(status_code=500, detail="Failed to get Autoptic endpoint. Database error.")

# delete autoptic endpoint
@router.delete("/delete_autoptic_endpoint")
async def delete_autoptic_endpoint(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_endpoint_by_id(user.id, None)
    return success

# Environment file

#update autoptic variables
@router.post("/new_autoptic_environment")
async def update_autoptic_environment(environment_update : AutopticEnvironment, user=Depends(get_current_user)):
    try:
        success = Users.update_user_autoptic_environment_by_id(user.id, 
                                                               environment_update.autoptic_environment,
                                                               environment_update.envFileName)
        if success:
            return {
                "autoptic_environment": environment_update.autoptic_environment,
            }
    except Exception as e:
        logger.error(" Failed to update Autoptic environment file. %s", e)
        raise HTTPException(status_code=500, detail="Failed to update Autoptic environment file. Database error.")

# get autoptic environment
@router.get("/get_autoptic_environment")
async def get_autoptic_environment(user=Depends(get_current_user)):
    try:
        autoptic_environment = Users.get_user_autoptic_environment_by_id(user.id)
        if autoptic_environment:
            return {
                "autoptic_environment": autoptic_environment,
            }
        return {
            "autoptic_environment": '',
        }
    except Exception as e:
        logger.error(" Failed to get Autoptic environment file. %s", e)
        raise HTTPException(status_code=500, detail="Failed to get Autoptic environment file. Database error.")  

# delete autoptic variables
@router.delete("/delete_autoptic_environment")
async def delete_autoptic_environment(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_environment_by_id(user.id, None,None)
    return success

# get autoptic environment
@router.get("/get_envFileName")
async def get_envFileName(user=Depends(get_current_user)):
    try:
        envFileName = Users.get_user_envFileName_by_id(user.id)
        if envFileName:
            return {
                "envFileName": envFileName,
            }
        return {
            "envFileName": '',
        }
    except Exception as e:
        logger.error(" Failed to get Autoptic environment file name. %s", e)
        raise HTTPException(status_code=500, detail="Failed to get Autoptic environment file name. Database error.")  
    
