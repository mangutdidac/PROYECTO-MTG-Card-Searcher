from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Ruta absoluta al directorio actual (backend/app/core)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Subimos dos niveles: backend/app/
APP_DIR = os.path.dirname(BASE_DIR)

# Ruta a la base de datos SQLite
DATABASE_URL = f"sqlite:///{APP_DIR}/core/mtg_underdeck.db"

# Engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite + FastAPI
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa
Base = declarative_base()


# Dependencia para usar en FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
