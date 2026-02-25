from sqlalchemy import Column, Integer, String, DateTime, func
from backend.app.core.database import Base


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = {"extend_existing": True}  # evita errores de índices duplicados


    id = Column(Integer, primary_key=True, index=True)

    # ID de la carta en Scryfall
    card_id = Column(String, unique=True, index=True, nullable=False)

    # Nombre de la carta (para mostrar rápido sin reconsultar)
    name = Column(String, nullable=False)

    # URL de la imagen normal
    image_url = Column(String, nullable=True)

    # Fecha de añadido a favoritos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
