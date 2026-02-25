# backend/app/api/favorites.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.favorites import Favorite

router = APIRouter()

@router.get("/favorites")
def get_favorites(db: Session = Depends(get_db)):
    return db.query(Favorite).all()
