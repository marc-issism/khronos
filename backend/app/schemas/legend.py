from pydantic import BaseModel, ConfigDict, Field

class LegendItem(BaseModel):
  key: str
  color: str = Field(min_length=3, max_length=7)

class LegendBase(BaseModel):
  user_id: str
  legend: list[LegendItem]

class LegendCreate(LegendBase):
  pass

class LegendResponse(LegendBase):
  model_config = ConfigDict(from_attributes=True) # allow to read as dot notation
  id: int
  date_posted: str