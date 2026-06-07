from __future__ import annotations
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, ARRAY, JSON, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

#TODO: modularize this file into a /models folder

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) # TODO: Change to Uuid
  username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # nullable=False means required field
  email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
  password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

  legend: Mapped[list[Legend]] = relationship(back_populates="user", cascade="all, delete-orphan") # user.legend
  activities: Mapped[list[Activity]] = relationship(back_populates="user", cascade="all, delete-orphan") # user.activities


# ex: GET /legend fetches all legend items for current user
class Legend(Base):
  __tablename__ = 'legends'
  
  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"), # id col in users table
    nullable=False,
    index=True
  )

  key: Mapped[str] = mapped_column(String(25), nullable=False)
  color: Mapped[str] = mapped_column(String(7))

  __table_args__ = (UniqueConstraint('user_id','key', name='user_legend_uc'),)

  user: Mapped[User] = relationship(back_populates="legend")


# ex: GET /activities/2026-05-31 fetches all activities for that date for current user
class Activity(Base):
  __tablename__ = "activities"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id"), # id col in users table
    nullable=False,
    index=True
  )
  legend_key: Mapped[str] = mapped_column(
    ForeignKey("legends.key"),
    nullable=False,
    index=True
  )
  date: Mapped[datetime] = mapped_column(DateTime(timezone=True)) 
  start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True)) 
  end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True)) 

  user: Mapped[User] = relationship(back_populates="activities")


# class Day(Base):
#   __tablename__ = 'days'

#   id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
#   user_id: Mapped[int] = mapped_column(
#     ForeignKey("users.id"), # id col in users table
#     nullable=False,
#     index=True
#   )

#   date: Mapped[datetime] = mapped_column(
#     DateTime(timezone=True),
#   )
#   activities: Mapped[list[dict]] = mapped_column(JSON, nullable=False) #ARRAY only works for Postgres
#   date_posted: Mapped[datetime] = mapped_column(
#     DateTime(timezone=True),
#     default=lambda: datetime.now(UTC)
#   )

#   user: Mapped[User] = relationship(back_populates='days') # MANY -> ONE: day.user