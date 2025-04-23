from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from app.auth import (
    create_access_token,
    set_admin_password,
    secrets_file_exists,
    get_secrets_path,
    SECRETS_FILE
)
from app.bundler import StaticBundler

router = APIRouter(tags=["Setup"])
templates = Jinja2Templates(directory="templates")

class SetupForm(BaseModel):
    username: str
    password: str
    confirm_password: str

@router.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    if secrets_file_exists():
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    bundler = StaticBundler(
        template_path="static/auth/setup.html",
        scripts_dir="static/auth/scripts",
        styles_dir="static/auth/styles"
    )
    return bundler.generate_html()

@router.post("/setup")
async def setup_admin_account(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if secrets_file_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin account already exists"
        )
    
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    set_admin_password(password)
    
    return {
        "status": "success",
        "message": "Admin account created successfully"
    }

@router.get("/check-setup")
async def check_setup():
    return {
        "initialized": secrets_file_exists()
    }