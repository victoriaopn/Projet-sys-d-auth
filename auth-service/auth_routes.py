"""
Routes de P2 : register, login, refresh-token, logout.
Le JWT (access token) et le refresh token sont posés en cookies HttpOnly
(pas accessibles en JS → protège contre le vol de token via XSS).
"""
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from sqlalchemy.orm import Session

from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_valid_refresh_token,
    hash_password,
    revoke_refresh_token,
    verify_password,
)
from app.database import get_db
from app.models import User
from app.schemas import LoginSchema, TokenResponse, UserCreate, UserOut

router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")

    db_user = User(
        email=user.email,
        password_hash=hash_password(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginSchema, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        # message volontairement générique : on ne dit pas si c'est l'email ou le mdp qui cloche
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user, db)

    # Cookies HttpOnly : inaccessibles en JS, envoyés automatiquement par le navigateur
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        # secure=True,  # à activer dès que vous servez en HTTPS (recommandé pour la démo finale)
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax",
    )

    return TokenResponse(access_token=access_token)


@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token_route(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Pas de refresh token")

    db_token = get_valid_refresh_token(refresh_token, db)
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")

    new_access_token = create_access_token(user)
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
    )
    return TokenResponse(access_token=new_access_token)


@router.post("/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token:
        revoke_refresh_token(refresh_token, db)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Déconnecté"}


@router.get("/users/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Exemple de route protégée : démontre que get_current_user fonctionne."""
    return current_user
