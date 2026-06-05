from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.schemas.user import UserResponse, UserCreate, UserUpdate
from app.database import DB
import app.models as models

# from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from sqlalchemy.orm import selectinload


# await db.refresh(user, attribute_names=["activities"]) when refreshing with relation

user_router = APIRouter(
  prefix='/users'
)

@user_router.get(
  '/'
)
async def get_users(db: DB):
  result = await db.execute(select(models.User))

  return result.scalars().all()


@user_router.post(
  '/',
  response_model=UserResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_user(user: UserCreate, db: DB):
  result = await db.execute(select(models.User).where(models.User.username == user.username))
  existing_user = result.scalars().first()

  if existing_user:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Username already exists"
    )
  
  result = await db.execute(select(models.User).where(models.User.email == user.email))
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
  await db.commit() # executes insert and saves
  await db.refresh(new_user) 

  return new_user


@user_router.get(
  '/{user_id}',
  status_code=status.HTTP_200_OK
)
async def get_user_from_id(user_id: int, db: DB):
  result = await db.execute(select(models.User).where(models.User.id == user_id))
  if not result:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="User does not exist"
    )
  return result.scalars().first()


@user_router.put(
  '/{user_id}',
  response_model=UserResponse,
  status_code=status.HTTP_200_OK
)
async def replace_user(
  user_id: int,
  user: UserCreate,
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


@user_router.patch(
  '/{user_id}',
  response_model=UserResponse,
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

