# backend/app/core/init_db.py

import os
import shutil
from backend.app.core.database import Base, engine

# 1️⃣ Ruta a la base de datos
DB_PATH = os.path.join(os.path.dirname(__file__), "mtg_underdeck.db")

# 2️⃣ Borrar base de datos vieja
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"Deleted old database at {DB_PATH}")

# 3️⃣ Limpiar __pycache__
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend/app/
for root, dirs, files in os.walk(PROJECT_ROOT):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
print("Cleared all __pycache__ directories.")

# 4️⃣ Importar modelos después de limpiar todo (evita circular imports)
from backend.app.models.favorites import Favorite
from backend.app.models.deck import Deck
from backend.app.models.deck_card import DeckCard

# 5️⃣ Crear tablas con extend_existing=True en cada modelo
Base.metadata.create_all(bind=engine)
print("Database initialized and tables created successfully!")
