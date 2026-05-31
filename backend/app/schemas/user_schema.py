from typing import Annotated

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class User(BaseModel):
  #TODO: spilt into private and public
  username: str = Field(min_length=1, max_length=50)
  email: EmailStr = Field(max_length=120)

class UserCreate(User):
  #TODO: password
  pass

class UserResponse(User):
  #TODO: exclude email
  model_config = ConfigDict(from_attributes=True)
  id: int

class UserUpdate(BaseModel):
  username: str | None = Field(default=None, min_length=1, max_length=50)
  email: EmailStr | None = Field(default=None, max_length=120)