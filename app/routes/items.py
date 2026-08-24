from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import Item, ItemCreate, ItemRead, utcnow

router = APIRouter(prefix="/item", tags=["Items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_session)):
    Item = Item.model_validate(payload)
    # # check if Item with the same name already exists
    existing_Item = db.exec(select(Item).where(Item.name == Item.name)).first()
    if existing_Item:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item with name '{Item.name}' already exists"
        )
    db.add(Item)
    db.commit()
    db.refresh(Item)
    return Item

