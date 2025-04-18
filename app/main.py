# The FastAPI stuff~

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from app.crud import get_page_by_slug, list_pages
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin_route, aina_route, aiconfig_route
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="AmiyaCMS",
    description="A cute tiny little CMS for smol projects",
    version="0.1.0",
)

templates = Jinja2Templates(directory="templates")

# Include Routers

app.include_router(admin_route.router)
app.include_router(aina_route.router)
app.include_router(aiconfig_route.router)

# Static assets (if you need to serve logos, favicons, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow your local admin tools to talk to it (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root: simple welcome or site list
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    pages = list_pages()
    return templates.TemplateResponse("index.html", {"request": request, "pages": pages})

# Dynamic route to serve saved pages as raw HTML
@app.get("/site/{slug}", response_class=HTMLResponse)
async def render_site(slug: str):
    page = get_page_by_slug(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return HTMLResponse(content=page.html, status_code=200)

# Admin Route
@app.get("/admin", response_class=FileResponse)
async def admin_ui():
    return FileResponse("static/admin-panel/index.html")

# Just in case someone want to add SPA functionality
@app.get("/api/site/{slug}")
async def api_site(slug: str):
    page = get_page_by_slug(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.__dict__

