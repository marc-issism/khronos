from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

POSTS: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

LEGENDS: list[dict] = [
  {
    "user_id": 0,
    "legend": [
      {
        "key": "sleep",
        "color": "#000"
      },
      {
        "key": "transportation",
        "color": "#fff"
      }
    ] 
  },
  {
    "user_id": 1,
    "legend": [
      {
        "key": "exercise",
        "color": "#123"
      },
      {
        "key": "work",
        "color": "#f0f"
      }
    ] 
  }
]

DAYS: list[dict] = [
  {
    "user_id": 0,
    "date": "2025-01-01",
    "activities": [
      {
        "start_time": "10:00pm",
        "end_time": "11:30pm",
        "legend_key": "transportation"
      },
      {
        "start_time": "9:00pm",
        "end_time": "10:00pm",
        "legend_key": "sleep"
      }
    ]
  },
  {
    "user_id": 0,
    "date": "2025-01-02",
    "activities": [
      {
        "start_time": "10:00pm",
        "end_time": "11:30pm",
        "legend_key": "transportation"
      },
      {
        "start_time": "9:00pm",
        "end_time": "10:00pm",
        "legend_key": "sleep"
      }
    ]
  }
]


@app.get('/', response_class=HTMLResponse)
def root():
  return f"<h1 style='text-align:center;'>FastAPI for Khronos</h1>"

@app.get('/legends')  
def get_legends():
  return LEGENDS

@app.get('/days')
def get_days():
  return DAYS

@app.get('/users/{user_id}/legend')
def get_user_legend(user_id: int):
  for legend in LEGENDS:
    if legend["user_id"] == user_id:
      return legend
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

@app.get('/users/{user_id}/days')
def get_user_days(user_id: int):
  days = []
  for day in DAYS:
    if day["user_id"] == user_id:
      days.append(day)

  if (len(days) == 0):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User has no day data or user does not exist")
  
  return days


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