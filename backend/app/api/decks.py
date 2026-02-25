from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models import Deck, DeckCard

router = APIRouter(prefix="/api/decks", tags=["Decks"])


# -------------------------
# Listar mazos
# -------------------------
@router.get("")
def list_decks(db: Session = Depends(get_db)):
    decks = db.query(Deck).all()
    # Serialize minimal info for listing
    return [
        {
            "id": d.id,
            "name": d.name,
            "description": d.description,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in decks
    ]


# -------------------------
# Crear mazo
# -------------------------
@router.post("")
def create_deck(name: str, db: Session = Depends(get_db)):
    if db.query(Deck).filter(Deck.name == name).first():
        raise HTTPException(status_code=400, detail="Deck already exists")

    deck = Deck(name=name)
    db.add(deck)
    db.commit()
    db.refresh(deck)
    return deck


# -------------------------
# Ver mazo con cartas
# -------------------------
@router.get("/{deck_id}")
def get_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    # Serialize deck and its cards to plain dicts for stable JSON responses
    return {
        "id": deck.id,
        "name": deck.name,
        "description": deck.description,
        "created_at": deck.created_at.isoformat() if deck.created_at else None,
        "cards": [
            {
                "id": c.id,
                "card_id": c.card_id,
                "card_name": c.card_name,
                "image_url": c.image_url,
                "quantity": c.quantity,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in deck.cards
        ],
    }


# -------------------------
# Eliminar mazo
# -------------------------
@router.delete("/{deck_id}")
def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    db.delete(deck)
    db.commit()
    return {"ok": True}


# -------------------------
# Añadir carta al mazo
# -------------------------
@router.post("/{deck_id}/cards")
def add_card_to_deck(
    deck_id: int,
    card_id: str,
    name: str,
    image_url: str | None = None,
    mana_cost: str | None = None,
    colors: str | None = None,
    type_line: str | None = None,
    db: Session = Depends(get_db),
):
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")

    card = (
        db.query(DeckCard)
        .filter(
            DeckCard.deck_id == deck_id,
            DeckCard.card_id == card_id
        )
        .first()
    )

    if card:
        if card.quantity >= 4:
            raise HTTPException(
                status_code=400,
                detail="Maximum 4 copies per card"
            )
        card.quantity += 1
    else:
        card = DeckCard(
            deck_id=deck_id,
            card_id=card_id,
            card_name=name,
            image_url=image_url,
            # DeckCard currently stores card_name and image_url only.
            quantity=1,
        )
        db.add(card)

    db.commit()
    # return serialized card
    return {
        "id": card.id,
        "deck_id": card.deck_id,
        "card_id": card.card_id,
        "card_name": card.card_name,
        "image_url": card.image_url,
        "quantity": card.quantity,
        "created_at": card.created_at.isoformat() if card.created_at else None,
    }


# -------------------------
# Cambiar cantidad de carta
# -------------------------
@router.patch("/cards/{deck_card_id}")
def update_card_quantity(
    deck_card_id: int,
    quantity: int,
    db: Session = Depends(get_db),
):
    if quantity < 1 or quantity > 4:
        raise HTTPException(status_code=400, detail="Quantity must be 1-4")

    card = db.query(DeckCard).filter(
        DeckCard.id == deck_card_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.quantity = quantity
    db.commit()
    return {
        "id": card.id,
        "deck_id": card.deck_id,
        "card_id": card.card_id,
        "card_name": card.card_name,
        "image_url": card.image_url,
        "quantity": card.quantity,
        "created_at": card.created_at.isoformat() if card.created_at else None,
    }


# -------------------------
# Quitar carta del mazo
# -------------------------
@router.delete("/cards/{deck_card_id}")
def remove_card_from_deck(
    deck_card_id: int,
    db: Session = Depends(get_db),
):
    card = db.query(DeckCard).filter(
        DeckCard.id == deck_card_id
    ).first()

    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    db.delete(card)
    db.commit()
    return {"ok": True}
