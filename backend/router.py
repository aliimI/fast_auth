from fastapi import APIRouter, Body, HTTPException, status
from typing import Annotated
from fastapi.responses import RedirectResponse

from state_storage import state_storage
from oauth_google import generate_google_oauth_redirect_uri

from config import settings

import aiohttp
import jwt

router = APIRouter(prefix="/auth")


@router.get("/google/url")
def get_google_oauth_redirect_uri():
    uri = generate_google_oauth_redirect_uri()
    return RedirectResponse(url=uri, status_code=302)

@router.post("/google/callback")
async def handle_code(
    code: Annotated[str, Body()],
    state: Annotated[str, Body()],
):
    if state not in state_storage:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired state"
        )
    else:
        print("State ok")
    google_token_url = "https://oauth2.googleapis.com/token"

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url=google_token_url,
            data={
                "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "redirect_uri": "http://localhost:3000/auth/google",
                "code": code,
            },
            ssl=False,
        ) as response:
            res = await response.json()
            print(f"{res=}")
            id_token = res["id_token"]
            access_token = res["access_token"]
            user_data = jwt.decode(
                id_token,
                algorithms=["RS256"],
                options={"verify_signature": False},
            )

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url="https://www.googleapis.com/drive/v3/files",
            headers={
                "Authorization": f"Bearer {access_token}"
            },
            ssl=False,
        ) as response:
            res = await response.json()
            print(f"{res=}")
            files = [item["name"] for item in res["files"]]

    return {
        "user": user_data,
        "files": files,
    }