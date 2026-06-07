from typing import Annotated

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserPublic(BaseModel):
  model_config = ConfigDict(from_attributes=True)
  id: int
  username: str = Field(min_length=1, max_length=50)

class UserPrivate(UserPublic):
  email: EmailStr = Field(max_length=120)

class UserCreate(UserPrivate):
  password: str = Field(min_length=8)
  pass

class Token(BaseModel):
  access_token: str
  token_type: str

# class UserResponse(UserPublic):
#   #TODO: exclude email
#   model_config = ConfigDict(from_attributes=True)
#   id: int

class UserUpdate(BaseModel):
  username: str | None = Field(default=None, min_length=1, max_length=50)
  email: EmailStr | None = Field(default=None, max_length=120)