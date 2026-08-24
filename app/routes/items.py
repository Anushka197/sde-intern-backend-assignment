from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import Item, ItemCreate, ItemRead, ItemUpdate, utcnow

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, db: Session = Depends(get_session)):
    item = Item.model_validate(payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=List[ItemRead])
def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    statement = select(Item).offset(skip).limit(limit)
    return db.exec(statement).all()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item {item_id} not found"
        )
    return item


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int, 
    payload: ItemUpdate, 
    db: Session = Depends(get_session)
):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item {item_id} not found"
        )
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    item.updated_at = utcnow()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Item {item_id} not found"
        )
    db.delete(item)
    db.commit()
    return None