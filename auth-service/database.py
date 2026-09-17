"""
Configuration de la base de données (SQLAlchemy).
Pour l'instant : SQLite (fichier local sso.db). Migration PostgreSQL possible plus tard
en changeant juste DATABASE_URL.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./sso.db"

# check_same_thread=False est nécessaire seulement pour SQLite (multi-threads FastAPI)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dépendance FastAPI : ouvre une session BDD par requête, la ferme ensuite."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
