from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/main.html", "r") as f:
        html = f.read()
    return html
    
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
