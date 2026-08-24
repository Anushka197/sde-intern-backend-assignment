from datetime import datetime, timezone
from enum import Enum
from pydantic import EmailStr
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional


def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Example Enum for reference
class ItemStatus(str, Enum):
    OPTION1 = "OPTION1"
    OPTION2 = "OPTION2"

# ==========================================
# DEMO MODELS (Parent & Child Relationship)
# ==========================================
class ItemBase(SQLModel):
    name: str = Field(min_length=1, max_length=100, index=True)
    description: str | None = Field(default=None, max_length=255)
    status: ItemStatus = Field(default=ItemStatus.OPTION1)


class Item(ItemBase, table=True):
    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=utcnow, nullable=False)


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ItemUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    status: ItemStatus | None = None