from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

#TODO: add date_created to ActivityUpdate

class Activity(BaseModel):
  legend_key: str
  date: datetime
  start_time: datetime
  end_time: datetime

class ActivityCreate(Activity):
  pass

class ActivityResponse(Activity):
  user_id: int
  model_config = ConfigDict(from_attributes=True)

class ActivityUpdate(ActivityCreate):
  pass

