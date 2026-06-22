### 3 layers of the application
# 1. database models (SQLAlchemy) -> stores/receives data
# 2. pydantic schemas -> validates request
# 3. API routes (endpoints) 

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from sqlalchemy.ext.asyncio  import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import Base, engine

from app.routers.users import user_router
from app.routers.legends import legends_router
from app.routers.activities import activities_router

#TODO: add status code to all routes
#TODO: add authorizations to all routes
#TODO: add more route options
#TODO: add pagination: https://www.youtube.com/watch?v=f1zggIOxmJg&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=13
#TODO: reset password/email, sending emails, account page: https://www.youtube.com/watch?v=4HxjBvZMAg8&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI&index=14


@asynccontextmanager
async def lifespan(_app: FastAPI):
  # startup
  yield
  # shutdown
  await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(legends_router)
app.include_router(activities_router)

@app.get('/', response_class=HTMLResponse)
def root():
  return f"<h1 style='text-align:center;'>FastAPI for Khronos</h1>"