from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

class Legend(BaseModel):
  user_id: int
  key: str
  color: str

class LegendCreate(Legend):
  pass

class LegendResponse(Legend):
  model_config = ConfigDict(from_attributes=True)

class LegendUpdate(LegendCreate):
  pass