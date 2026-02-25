from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class DeckCard(Base):
    __tablename__ = "deck_card"
    # extend_existing keeps development reloads safe
    __table_args__ = (
        UniqueConstraint("deck_id", "card_id", name="uq_deck_card"),
        CheckConstraint("quantity >= 1 AND quantity <= 4", name="check_quantity_range"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)

    deck_id = Column(
        Integer,
        ForeignKey("decks.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ID de Scryfall
    card_id = Column(String, nullable=False, index=True)

    card_name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    quantity = Column(Integer, nullable=False, default=1)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    deck = relationship("Deck", back_populates="cards")
