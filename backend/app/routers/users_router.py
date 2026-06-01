
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import Session

from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate
from app.database import get_db
import app.models as models

DB = Annotated[Session, Depends(get_db)]

user_router = APIRouter(
  prefix='/users'
)

@user_router.get(
  '/',
  include_in_schema=False,
)
def get_users(db: DB):
  result = db.execute(select(models.User)).scalars().all()
  return result


@user_router.post(
  '/',
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: DB):
  result = db.execute(select(models.User).where(models.User.username == user.username))
  existing_user = result.scalars().first()

  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Username already exists"
    )
  
  result = db.execute(select(models.User).where(models.User.email == user.email))
  existing_email = result.scalars().first()

  if existing_email:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Email already exists"
    )
  
  new_user = models.User(
    username=user.username,
    email=user.email
  )

  db.add(new_user) # stages insert
  db.commit() # executes insert and saves
  db.refresh(new_user) # 

  return new_user


@user_router.get(
  '/{user_id}',
  include_in_schema=False,
  status_code=status.HTTP_200_OK
)
def get_user_from_id(user_id: int, db: DB):
  result = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  return result


@user_router.put(
  '/{user_id}',
  response_model=UserResponse,
  status_code=status.HTTP_200_OK
)
def replace_user(
  user_id: int,
  user: UserCreate,
  db: DB
):
  existing_user = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  existing_user.username = user.username
  existing_user.email = user.email
  db.commit()
  db.refresh(existing_user)
  return existing_user


@user_router.patch(
  '/{user_id}',
  response_model=UserResponse,
  status_code=status.HTTP_200_OK
)
def patch_user(
  user_id: int,
  user: UserUpdate,
  db: DB
):
  existing_user = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  
  user = user.model_dump(exclude_unset=True) # leave empty attributes unchanged
  for field, value in user.items():
    setattr(existing_user, field, value)

  db.commit()
  db.refresh(existing_user)
  return existing_user


@user_router.delete(
  '/{user_id}',
  status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(
  user_id: int,
  db: DB
):
  existing_user = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  db.delete(existing_user)
  db.commit()


#TODO: fix this 
@user_router.get('/{user_id}/activities', include_in_schema=False, status_code=status.HTTP_200_OK)
def get_activities_by_user_id(user_id: int, db:DB):
  existing_user = db.execute(select(models.User).where(models.User.id == user_id)).scalars().first()
  if not existing_user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  result = db.execute(select(models.User.activities)).scalars().all()
  return result