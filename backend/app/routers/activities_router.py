from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import Session

from app.schemas.activity_schema import ActivityResponse, ActivityCreate, ActivityUpdate
from app.database import get_db
import app.models as models

DB = Annotated[Session, Depends(get_db)]

activities_router = APIRouter(
  prefix='/activities'
)

@activities_router.get(
  '/',
  include_in_schema=False
)
def get_activities(db: DB):
  result = db.execute(select(models.Activity)).scalars().all()
  return result


@activities_router.post(
  '/',
  response_model=ActivityResponse,
  status_code=status.HTTP_201_CREATED
)
def create_activity(activity: ActivityCreate, db: DB):
  #TODO: Exception handling
  new_activity = models.Activity(
    user_id = activity.user_id,
  legend_key = activity.legend_key,
  date = activity.date,
  start_time = activity.start_time,
  end_time = activity.end_time
  )

  db.add(new_activity)
  db.commit()
  db.refresh(new_activity)

  return new_activity
  