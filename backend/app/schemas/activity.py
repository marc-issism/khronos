from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

class Activity(BaseModel):
  user_id: int
  legend_key: str
  date: datetime
  start_time: datetime
  end_time: datetime

class ActivityCreate(Activity):
  pass

class ActivityResponse(Activity):
  model_config = ConfigDict(from_attributes=True)

class ActivityUpdate(ActivityCreate):
  pass