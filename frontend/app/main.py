from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers.pages_routes import router

app = FastAPI(title="Les Jetons Fiscaux — Démonstration")
app.mount("/static", StaticFiles(directory=Path(__file__).resolve().parent / "static"), name="static")
app.include_router(router)
