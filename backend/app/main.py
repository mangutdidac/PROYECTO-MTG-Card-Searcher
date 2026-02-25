from fastapi import FastAPI

from backend.app.api import decks
from .api import cards
from .api.v1 import sets 
from .api import cards, favorites
from backend.app.core.database import SessionLocal

app = FastAPI(title="Magic Analytics API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(cards.router)
app.include_router(cards.router, prefix="/api/v1/cards", tags=["Cards"])
app.include_router(sets.router, prefix="/api/v1/sets", tags=["Sets"])  # ✅ sets router
app.include_router(favorites.router, prefix="/api", tags=["Favorites"])
app.include_router(decks.router)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
