"""Models package for the application.

This module exposes the model classes so that importing
`backend.app.models` registers them with SQLAlchemy's metadata
without executing unrelated side-effects (like deleting files).
"""

from backend.app.core.database import Base, engine

# Import model modules so their classes are registered on Base.metadata
from .deck import Deck
from .deck_card import DeckCard
from .favorites import Favorite

__all__ = ["Deck", "DeckCard", "Favorite", "Base", "engine"]
