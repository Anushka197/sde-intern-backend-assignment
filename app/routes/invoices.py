from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from uuid import UUID

from app.database import get_session
from app.models import InvoiceCreate, InvoiceRead, utcnow

router = APIRouter(prefix="/invoice", tags=["Invoices"])

@router.post("",response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_session)):
    invoice = InvoiceCreate.model_validate(payload)
    # # check if invoice with the same id already exists
    existing_invoice = db.exec(select(InvoiceCreate).where(InvoiceCreate.id == invoice.id)).first()
    if existing_invoice:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invoice with id '{invoice.id}' already exists"
        )
    statement = select()
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice
