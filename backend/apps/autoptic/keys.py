from fastapi import Depends, APIRouter
from fastapi import HTTPException
from pydantic import BaseModel

from apps.webui.models.users import Users

from utils.utils import (
    get_current_user,
)

router = APIRouter()

############################
# Autoptic Keys
############################

#JERE: the functions are ok, but I need to manage errors in the next version.

#update autoptic endpoint
@router.post("/new_autoptic_endpoint")
async def update_autoptic_endpoint(autoptic_endpoint: dict, user=Depends(get_current_user)):
    try:
        success = Users.update_user_autoptic_endpoint_by_id(user.id, autoptic_endpoint["autoptic_endpoint"])
        if success:
            return {
                "autoptic_endpoint": autoptic_endpoint["autoptic_endpoint"],
            }

    except:
        raise HTTPException(500) #acá deberíamos poner algo como mensaje o error
    
# get autoptic endpoint
@router.get("/get_autoptic_endpoint")
async def get_autoptic_endpoint(user=Depends(get_current_user)):
    autoptic_endpoint = Users.get_user_autoptic_endpoint_by_id(user.id)
    if autoptic_endpoint:
        return {
            "autoptic_endpoint": autoptic_endpoint,
        }
    else:
        raise HTTPException(404)
        
# delete autoptic endpoint
@router.delete("/delete_autoptic_endpoint")
async def delete_autoptic_endpoint(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_endpoint_by_id(user.id, None)
    return success

# JERE: When the keys are empty there is a 404 error (even with the original OWUI API key). Maybe I can fix this.

class AutopticEnvironment(BaseModel):
    autoptic_environment: str
    envFileName: str

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
    except:
        raise HTTPException(500)

# get autoptic environment
@router.get("/get_autoptic_environment")
async def get_autoptic_environment(user=Depends(get_current_user)):
    autoptic_environment = Users.get_user_autoptic_environment_by_id(user.id)
    if autoptic_environment:
        return {
            "autoptic_environment": autoptic_environment,
        }
    else:
        raise HTTPException(404)    

# delete autoptic variables
@router.delete("/delete_autoptic_environment")
async def delete_autoptic_environment(user=Depends(get_current_user)):
    success = Users.update_user_autoptic_environment_by_id(user.id, None,None)
    return success

# get autoptic environment
@router.get("/get_envFileName")
async def get_envFileName(user=Depends(get_current_user)):
    envFileName = Users.get_user_envFileName_by_id(user.id)
    if envFileName:
        return {
            "envFileName": envFileName,
        }
    else:
        raise HTTPException(404)    
