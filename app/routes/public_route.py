from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.crud import list_pages

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/main.html", "r") as f:
        html = f.read()
    return html

# Root: simple welcome or site list
@router.get("/wisata", response_class=HTMLResponse)
async def home(request: Request):
    pages = list_pages()
    return templates.TemplateResponse("wisata.html", {"request": request, "pages": pages})
    
@router.get("/sejarah", response_class=HTMLResponse)
async def sejarah_main():
    with open("templates/sejarah.html", "r") as f:
        html = f.read()
    return html

@router.get("/geografi", response_class=HTMLResponse)
async def geografi_main():
    with open("templates/geografi.html", "r") as f:
        html = f.read()
    return html

@router.get("/budaya", response_class=HTMLResponse)
async def budaya_main():
    with open("templates/budaya.html", "r") as f:
        html = f.read()
    return html
