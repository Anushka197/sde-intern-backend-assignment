from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import Customer, CustomerCreate, CustomerRead, utcnow

router = APIRouter(prefix="/customer", tags=["Customers"])


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_session)):
    customer = Customer.model_validate(payload)
    # # check if customer with the same name already exists
    existing_customer = db.exec(select(Customer).where(Customer.name == customer.name)).first()
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Customer with name '{customer.name}' already exists"
        )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/{id}", response_model=CustomerRead)
def get_customer(id: int, db: Session = Depends(get_session)):
    customer = db.get(Customer, id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Customer {id} not found"
        )
    return customer
