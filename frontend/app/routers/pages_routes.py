from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parents[1] / "templates")


@router.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/login", status_code=303)


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"page": "login"})


@router.get("/code-gmail")
def code_gmail(request: Request):
    return templates.TemplateResponse(request=request, name="code_gmail.html", context={"page": "code"})


# Public previews only: apply server-side authentication and role checks
# before connecting these pages to real user data.
@router.get("/rh")
def rh(request: Request):
    return templates.TemplateResponse(request=request, name="rh.html", context={"page": "rh"})


@router.get("/it")
def it(request: Request):
    return templates.TemplateResponse(request=request, name="it.html", context={"page": "it"})
