from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Deck(Base):
    __tablename__ = "decks"
    __table_args__ = {"extend_existing": True}  # evita errores de índices duplicados

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # optional owner/user field could be added later (user_id FK)

    # Relación con cartas del mazo
    cards = relationship(
        "DeckCard",
        back_populates="deck",
        cascade="all, delete-orphan"
    )
# DeckCard model moved to `deck_card.py` to avoid duplicate definitions.
