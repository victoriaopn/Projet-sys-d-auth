"""
Point d'entrée de l'application.
Lancer avec : uvicorn app.main:app --reload
Puis ouvrir http://127.0.0.1:8000/docs pour tester /register et /login
"""
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth_routes

# Crée les tables SQLite au démarrage si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DGFiP SSO — API d'authentification")

app.include_router(auth_routes.router)


@app.get("/")
def root():
    return {"message": "API SSO DGFiP — voir /docs pour tester"}
