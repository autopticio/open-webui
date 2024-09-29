import logging
import aiohttp
import httpx

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import HTTPException
from config import GO_AUTOPTIC_URL

class Payload(BaseModel):
    endpoint_id: str
    token_id: str

router = APIRouter()

# logger = logging.getLogger(__name__)

@router.post("/create_token")
async def createToken(credentials: Payload):
    try:
        async with httpx.AsyncClient(trust_env=True) as client:
            response = await client.post(
                f"{GO_AUTOPTIC_URL}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
            )
            text = response.text

            if response.status_code != 201:
                raise HTTPException(
                    status=response.status_code,
                    detail=f"Error from Go backend: {text}" # Change the 'Go backend'
                )

            return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong on OpenWeb UI. ERROR: {e}")

    
@router.get("/read_token")
# async def createToken(credentials: Payload):
async def createToken(endpoint_id: str,token_id: str):
    try:
        async with httpx.AsyncClient(trust_env=True) as client:
            response = await client.get(
                # f"{GO_AUTOPTIC_URL}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
                f"{GO_AUTOPTIC_URL}/story/ep/{endpoint_id}/token/{token_id}",
            )
            text = response.text

            if response.status_code != 200:
                raise HTTPException(
                    status=response.status_code,
                    detail=f"Error from Go backend: {text}" # Change the 'Go backend'
                )

            return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong on OpenWeb UI. ERROR: {e}")

    
@router.delete("/delete_token")
async def createToken(credentials: Payload):
    try:
        async with httpx.AsyncClient(trust_env=True) as client:
            response = await client.delete(
                f"{GO_AUTOPTIC_URL}/story/ep/{credentials.endpoint_id}/token/{credentials.token_id}",
            )
            text = response.text

            if response.status_code != 200:
                raise HTTPException(
                    status=response.status_code,
                    detail=f"Error from Go backend: {text}" # Change the 'Go backend'
                )

            return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong on OpenWeb UI. ERROR: {e}")
    
@router.get("/read_token_list")
async def createToken(endpoint_id: str):
    try:
        async with httpx.AsyncClient(trust_env=True) as client:
            response = await client.get(
                f"{GO_AUTOPTIC_URL}/story/ep/{endpoint_id}/token",
            )
            text = response.text

            if response.status_code != 200:
                raise HTTPException(
                    status=response.status_code,
                    detail=f"Error from Go backend: {text}" # Change the 'Go backend'
                )

            return text

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong on OpenWeb UI. ERROR: {e}")