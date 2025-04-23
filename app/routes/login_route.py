from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import timedelta
from app.auth import (
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user,
    SECRET_KEY,
    ALGORITHM,
)
from app.bundler import StaticBundler
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])

class LoginForm(BaseModel):
    username: str
    password: str
    remember_me: bool = False

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    bundler = StaticBundler(
        template_path="static/auth/login.html",
        scripts_dir="static/auth/scripts",
        styles_dir="static/auth/styles"
    )
    return bundler.generate_html()

@router.post("/login")
async def login_for_access_token(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    remember_me: bool = Form(False),
):
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    expires_in = timedelta(days=7) if remember_me else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=expires_in
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Enable in production with HTTPS
        samesite="lax",
        max_age=expires_in.total_seconds(),
    )
    
    return {"status": "success"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "success"}