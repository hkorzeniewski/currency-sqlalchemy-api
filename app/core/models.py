from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class TimestampAbstractModel(SQLModel):
    created_at: datetime = Field(nullable=False, sa_column=Column(DateTime, server_default=func.now()))
    updated_at: Optional[datetime] = Field(default=None, nullable=True, sa_column=Column(DateTime, onupdate=func.now()))
