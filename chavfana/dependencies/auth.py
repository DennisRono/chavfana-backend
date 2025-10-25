import uuid
from fastapi import Header, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Annotated

from pydantic import BaseModel
from chavfana.core.config import settings
from chavfana.core.logging import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")
GetToken = Annotated[str, Depends(oauth2_scheme)]


class UserData(BaseModel):
    sub: uuid.UUID
    role: str


async def get_current_user(token: GetToken):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        sub = payload.get("sub")
        role = payload.get("role")

        if not id or not sub or not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some credentials are Missing in Token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            return UserData(sub=sub, role=role)
        except (ValueError, TypeError) as e:
            print(f"Error creating UserData: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Couldnt validate token data against Schema",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except jwt.JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Token Decode Failed! {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


GetCurrentUser = Annotated[UserData, Depends(get_current_user)]


def get_auth_header(token: GetToken, client_name: str = Header(...)) -> dict:
    return {"Authorization": f"Bearer {token}", "Client-Name": f"{client_name.upper()}"}
