from datetime import datetime, timezone
from enum import Enum
from pydantic import EmailStr, BaseModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from uuid import UUID

def utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Example Enum for reference
class CategoryEnum(str, Enum):
    B2B = "b2b"
    B2C = "b2c"

# =====================================
# CUSTOMER MODELS
# ====================================

class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: UUID | None= Field(default=None, primary_key=True)
    name: str = Field(min_length=1, unique=True, index=True)
    category: CategoryEnum = Field(default=CategoryEnum.B2B)
    address: str
    opening_balance: float = Field(default=0.0, ge=0.0)


class CustomerCreate(SQLModel):
    name: str = Field(min_length=1, index=True)
    category: CategoryEnum = Field(default=CategoryEnum.B2B)
    address: str
    opening_balance: float = Field(default=0.0, ge=0.0)

class CustomerRead(Customer):
    pass


# =====================================
# ITEM MODELS
# ====================================

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: UUID | None= Field(default=None, primary_key=True)
    name: str = Field(min_length=1, index=True) # uniqueness imposed in the routes
    tax: float = Field(ge=0.0, le=28.0)

class ItemCreate(SQLModel):
    
    name: str = Field(min_length=1, index=True) # uniqueness imposed in the routes
    tax: float = Field(ge=0.0, le=28.0)

class ItemRead(Item):
    pass

# ===================================
# INVOICE MODELS
# ===================================


# def round_half_up(number, decimals=2):
#     d = Decimal(str(number))
#     exponent = Decimal('1.' + '0' * decimals) 
#     return d.quantize(exponent, rounding=ROUND_HALF_UP)

# def getValues(unit_price, item_tax, qty):
#     net_total : float = unit_price * qty
#     tax_applied = net_total*item_tax/100.0
#     tax_applied = round_half_up(tax_applied)
#     total = net_total + tax_applied
#     return [net_total, tax_applied, total]

# class StatusEnum(str, Enum):
#     DRAFT = "draft"
#     SUBMITTED = "submitted"

# class ItemsDict(SQLModel):
#     item_id: UUID = Field(unique=True)
#     unit_price: float = Field(ge=0)
#     qty: int = Field(ge=1)
#     net_total : float
#     tax_applied: float
#     total : float

# class InvoiceRead(SQLModel, table=True):
#     __tablename__ = "invoices"
#     id: UUID = Field(primary_key=True)
#     customer_id : UUID = Field(foreign_key="customers.id")
#     date: datetime
#     # items: List[ItemsDict] 
#     net_invoice: float
#     total_tax: float
#     grand_total: float
#     status: StatusEnum = Field(default=StatusEnum.DRAFT)

# class InvoiceCreate(SQLModel):
#     id: str
#     customer_id : UUID
#     date: date
#     items: List[ItemsDict]