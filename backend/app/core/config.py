from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import ENV

class Settings(BaseSettings):
  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8"
  )

  database_url: str
  secret_key: SecretStr

  algorithm: str = "HS256"
  access_token_expire_minutes: int = 30


SETTINGS = Settings() #TODO: use env
print(SETTINGS)