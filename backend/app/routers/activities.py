from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.database import DB
import app.models as models

from sqlalchemy.orm import selectinload
from app.schemas.activity import ActivityResponse, ActivityCreate, ActivityUpdate

from app.core.auth import CurrentUser

activities_router = APIRouter(
  prefix='/activities'
)

@activities_router.get(
  '/',
)
async def get_activities(db: DB):
  result = await db.execute(select(models.Activity))
  return result.scalars().all()


@activities_router.post(
'/',
  response_model=ActivityResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_activity(activity: ActivityCreate, current_user: CurrentUser, db: DB):
  new_activity = models.Activity(
    user_id = current_user.id,
    legend_key = activity.legend_key,
    date = activity.date,
    start_time = activity.start_time,
    end_time = activity.end_time
  )

  db.add(new_activity)
  await db.commit()
  await db.refresh(new_activity)

  return new_activity


@activities_router.put(
  '/{activity_id}',
  response_model=ActivityResponse
)
async def replace_activity(
  activity_id: int,
  activity_update: ActivityUpdate,
  current_user: CurrentUser,
  db: DB
):
  result = await db.execute(
    select(models.Activity).where(models.Activity.id == activity_id)
  )
  activity = result.scalars().first()

  if not activity:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Activity not found",
    )

  if current_user.id != activity.user_id:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Not authorized to perform this action"
    )

  activity.legend_key = activity_update.legend_key
  activity.date = activity_update.date
  activity.start_time = activity_update.start_time
  activity.end_time = activity_update.end_time

  await db.commit()
  await db.refresh(activity)

  return activity