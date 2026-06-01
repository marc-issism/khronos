### 3 layers of the application
# 1. database models (SQLAlchemy) -> stores/receives data
# 2. pydantic schemas -> validates request
# 3. API routes (endpoints) 

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine

from app.routers.users_router import user_router
from app.routers.legends_router import legends_router
from app.routers.activities_router import activities_router

Base.metadata.create_all(bind=engine)

# app.mount('/media', staticFiles(directory='media'), name='media') for serving files

app = FastAPI()
app.include_router(user_router)
app.include_router(legends_router)
app.include_router(activities_router)

@app.get('/', response_class=HTMLResponse)
def root():
  return f"<h1 style='text-align:center;'>FastAPI for Khronos</h1>"







  

# @app.post(
#   '/users',
#   response_model=UserResponse,
#   status_code=status.HTTP_201_CREATED
# )
# def get_users(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
#   pass

 

# @app.get('/legends', response_model=list[LegendResponse])  
# def get_legends():
#   return LEGENDS


# @app.get('/days', response_model=list[DayResponse])
# def get_days():
#   return DAYS

# @app.post('/days', response_model=DayResponse)
# def post_day(day: DayCreate):
#   new_day = {
#     "user_id": day.user_id,
#     "date": day.date,
#     "activities": day.activities
#   }
#   DAYS.append(new_day)
#   return new_day


# @app.get('/users/{user_id}/legend', response_model=LegendResponse)
# def get_user_legend(user_id: int):
#   for legend in LEGENDS:
#     if legend["user_id"] == user_id:
#       return legend
#   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")


# @app.post(
#   '/users/legends', 
#   response_model=LegendResponse, 
#   status_code=status.HTTP_201_CREATED
# )
# def create_legend(legend: LegendCreate):
#   new_id = max(legend["user_id"] for legend in LEGENDS) + 1 if LEGENDS else 1
#   new_legend = {
#     "user_id": new_id,
#     "legend": legend.legend
#   }
#   LEGENDS.append(new_legend)
#   return new_legend


# @app.get('/users/{user_id}/days', response_model=DayResponse)
# def get_user_days(user_id: int):
#   days = []
#   for day in DAYS:
#     if day["user_id"] == user_id:
#       days.append(day)

#   if (len(days) == 0):
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no day data or user does not exist")
  
#   return days

# @app.post(
#   '/users/{user_id}/days',
#   response_model=DayCreate,
#   status_code=status.HTTP_201_CREATED
# )
# def create_day_for_user(day: DayCreate, user_id:int):
#   new_day = {
#     "user_id": user_id,
#     "date": day.date,
#     "activities": day.activities
#   }
#   DAYS.append(new_day)
#   return new_day


## StarletteHTTPException Handler
# @app.exception_handler(StarletteHTTPException)
# def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
#     message = (
#         exception.detail
#         if exception.detail
#         else "An error occurred. Please check your request and try again."
#     )

#     if request.url.path.startswith("/users"):
#         return JSONResponse(
#             status_code=exception.status_code,
#             content={"detail": message},
#         )