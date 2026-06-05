from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.schemas.legend import LegendResponse, LegendCreate, LegendUpdate
from app.database import DB
import app.models as models

from sqlalchemy.orm import selectinload

legends_router = APIRouter(
  prefix='/legends'
)

@legends_router.get(
  '/'
)
async def get_legends(db: DB):
  results = await db.execute(select(models.Legend))
  return results.scalars().all()


@legends_router.post(
  '/',
  response_model=LegendResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_legend(legend: LegendCreate, db: DB):
  #TODO: add legend logic so unique per user (exeption handling)
  new_legend = models.Legend(
    user_id = legend.user_id,
    key = legend.key,
    color = legend.color
  )

  db.add(new_legend)
  await db.commit()
  await db.refresh(new_legend)

  return new_legend