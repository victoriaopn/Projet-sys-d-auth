"""
Modèles SQLAlchemy.
Pour l'instant : uniquement ce dont P2 a besoin (users + tokens de refresh).
P3 ajoutera otp_codes, roles/permissions. P5 ajoutera connection_logs.
"""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    role = Column(String, default="contribuable")  # utilisé plus tard par P3 pour le RBAC
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class RefreshToken(Base):
    """
    Stocke les refresh tokens émis, pour pouvoir les révoquer (logout, sécurité).
    On ne stocke jamais le token en clair : on garde son hash.
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    token_hash = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
