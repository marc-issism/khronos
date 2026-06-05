from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.database import DB
import app.models as models

from sqlalchemy.orm import selectinload
from app.schemas.activity import ActivityResponse, ActivityCreate, ActivityUpdate

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
async def create_activity(activity: ActivityCreate, db: DB):
  #TODO: Exception handling
  new_activity = models.Activity(
    user_id = activity.user_id,
  legend_key = activity.legend_key,
  date = activity.date,
  start_time = activity.start_time,
  end_time = activity.end_time
  )

  db.add(new_activity)
  await db.commit()
  await db.refresh(new_activity)

  return new_activity
  