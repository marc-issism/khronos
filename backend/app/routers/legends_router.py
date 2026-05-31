from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import Session

from app.schemas.legend_schema import LegendResponse, LegendCreate, LegendUpdate
from app.database import get_db
import app.models as models

DB = Annotated[Session, Depends(get_db)]

legends_router = APIRouter(
  prefix='/legends'
)

@legends_router.get(
  '/',
  include_in_schema=False
)
def get_legends(db: DB):
  results = db.execute(select(models.Legend)).scalars().all()
  return results


@legends_router.post(
  '/',
  response_model=LegendResponse,
  status_code=status.HTTP_201_CREATED
)
def create_legend(legend: LegendCreate, db: DB):
  #TODO: add legend logic so unique per user (exeption handling)
  new_legend = models.Legend(
    user_id = legend.user_id,
    key = legend.key,
    color = legend.color
  )

  db.add(new_legend)
  db.commit()
  db.refresh(new_legend)

  return new_legend