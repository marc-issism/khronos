from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.schemas.user import UserPrivate, UserPublic, UserCreate, UserUpdate, Token
from app.database import DB
import app.models as models

# from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from sqlalchemy.orm import selectinload

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import func # case insensitive queries

from app.core.auth import create_access_token, hash_password, oauth2_scheme, verify_access_token, verify_password

from app.core.config import SETTINGS



# await db.refresh(user, attribute_names=["activities"]) when refreshing with relation

user_router = APIRouter(
  prefix='/users'
)

@user_router.get(
  '/',
  # response_model=UserPublic
  response_model_include=UserPublic
)
async def get_users(db: DB):
  result = await db.execute(select(models.User))

  return result.scalars().all()


@user_router.post(
  '/',
  response_model=UserPrivate,
  status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate, db: DB):
  result = await db.execute(select(models.User).where(func.lower(models.User.username) == user.username.lower()))
  existing_user = result.scalars().first()

  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Username already exists"
    )
  
  result = await db.execute(select(models.User).where(func.lower(models.User.email) == user.email.lower()))
  existing_email = result.scalars().first()

  if existing_email:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already exists"
    )
  
  new_user = models.User(
    username=user.username,
    email=user.email.lower(),
    password_hash=hash_password(user.password)
  )

  db.add(new_user) # stages insert
  await db.commit() # executes insert and saves
  await db.refresh(new_user) 

  return new_user


@user_router.post(
    '/token',
    response_model=Token
)
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: DB
):
  # Look up user by email, OAuth2PasswordRequestForm uses "username" field but we will use that as email
  result = await db.execute(
    select(models.User).where(models.User.email == form_data.username.lower())
  )
  user = result.scalars().first()

  if not user or not verify_password(form_data.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  access_token_expiration = timedelta(minutes=SETTINGS.access_token_expire_minutes)
  access_token = create_access_token(
    data={"sub": str(user.id)},
    expires_delta=access_token_expiration
  )
  return Token(access_token=access_token, token_type="bearer") 


@user_router.get(
    '/me',
    response_model=UserPrivate
)
async def get_current_user(
  token: Annotated[str, Depends(oauth2_scheme)],
  db: DB
):
  user_id = verify_access_token(token)
  if user_id is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token",
      headers={"WWW-Authenticate": "Bearer"}
    )

  try:
    user_id_int = int(user_id)
  except (TypeError, ValueError):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid or expired token",
      headers={"WWW-Authenticate": "Bearer"}
    )
  
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


@user_router.get(
  '/{user_id}',
  status_code=status.HTTP_200_OK
)
async def get_user_from_id(user_id: int, db: DB):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  user = result.scalars().first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  return user


#TODO: Email and username checks 
@user_router.put(
  '/{user_id}',
  response_model=UserPrivate,
  status_code=status.HTTP_200_OK
)
async def replace_user(
  user_id: int,
  user: UserPrivate,
  db: DB
):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  existing_user = result.scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  existing_user.username = user.username
  existing_user.email = user.email
  await db.commit()
  await db.refresh(existing_user)
  return existing_user


#TODO: Email and username checks 
@user_router.patch(
  '/{user_id}',
  response_model=UserPrivate,
  status_code=status.HTTP_200_OK
)
async def patch_user(
  user_id: int,
  user: UserUpdate,
  db: DB
):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  existing_user = result.scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  
  user = user.model_dump(exclude_unset=True) # leave empty attributes unchanged
  for field, value in user.items():
    setattr(existing_user, field, value)

  await db.commit()
  await db.refresh(existing_user)
  return existing_user


@user_router.delete(
  '/{user_id}',
  status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
  user_id: int,
  db: DB
):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  existing_user = result.scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  await db.delete(existing_user)
  await db.commit()


@user_router.get(
  '/{user_id}/activities'
  , status_code=status.HTTP_200_OK
)
async def get_activities_by_user_id(user_id: int, db:DB):
  existing_user = await db.execute(select(models.User).where(models.User.id == user_id))
  if not existing_user.scalars().first():
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  result = await db.execute(select(models.User).options(selectinload(models.User.activities)))
  return result.scalars().all()

