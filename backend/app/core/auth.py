from datetime import UTC, datetime, timedelta

import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash

from app.core.config import SETTINGS
from app.database import DB
import app.models as models 

from typing import Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session

# 401 -> not authenticated
# 403 -> not allowed to do that action


LOGIN_PATH = "users/token"

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=LOGIN_PATH)


def hash_password(password: str) -> str:
  return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  return password_hash.verify(plain_password, hashed_password)
# encryption is reversible, hashing is not


# A JSON Web Token has 3 parts
# - Header -> algo and type
# - Payload -> data and expiration
# - signature -> proves no tampering
# ex-ish: ghriuygherwi32hi.rgbh43e9ougth9.892u4t8hgnn lmao

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
  """Create a JWT access token."""
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(UTC) + expires_delta
  else:
    expire = datetime.now(UTC) + timedelta(
      minutes=SETTINGS.access_token_expire_minutes
    )
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(
    to_encode,
    SETTINGS.secret_key.get_secret_value(),
    algorithm=SETTINGS.algorithm
  )
  return encoded_jwt


def verify_access_token(token: str) -> str | None:
  """Verify a JWT access token and return the subject (user id) if valid."""
  try:
    payload = jwt.decode(
      token, 
      SETTINGS.secret_key.get_secret_value(),
      algorithms=[SETTINGS.algorithm],
      options={"require": ["exp", "sub"]}
    )
  except jwt.InvalidTokenError:
    return None
  else:
    return payload.get("sub")


HttpExceptionInvalidToken = HTTPException(
  status_code=status.HTTP_401_UNAUTHORIZED,
  detail="Invalid or expired token",
  headers={"WWW-Authenticate": "Bearer"} 
)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: DB
) -> models.User :
  user_id = verify_access_token(token)
  if user_id is None:
    raise HttpExceptionInvalidToken
  
  try: 
    user_id_int = int(user_id)
  except (TypeError, ValueError):
    raise HttpExceptionInvalidToken
  
  result = await db.execute(
    select(models.User).where(models.User.id == user_id_int)
  )
  user = result.scalars().first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="User not found",
      headers={"WWW-Authenticate": "Bearer"} 
    )
  
  return user

# current user is a models.User object with metadata from get_current_user -> a class
CurrentUser = Annotated[models.User, Depends(get_current_user)]
