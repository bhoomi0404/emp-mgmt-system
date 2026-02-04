from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

router = APIRouter()

# locate frontend templates directory relative to backend
root = Path(__file__).resolve().parents[3]
templates_dir = os.path.join(root, "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})


@router.get("/employees", response_class=HTMLResponse)
def employees_page(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})
