# The FastAPI stuff~

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from app.crud import get_page_by_slug, list_pages
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin

app = FastAPI(
    title="AmiyaCMS",
    description="A cute tiny little CMS for smol projects",
    version="0.1.0",
)

# Include Routers

app.include_router(admin.router)

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
async def home():
    pages = list_pages()
    list_html = "<h1>Available Pages</h1><ul>"
    for page in pages:
        list_html += f'<li><a href="/site/{page.slug}">{page.title}</a></li>'
    list_html += "</ul>"
    return list_html

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
    return FileResponse("static/admin.html")

# Just in case someone want to add SPA functionality
@app.get("/api/site/{slug}")
async def api_site(slug: str):
    page = get_page_by_slug(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.__dict__

