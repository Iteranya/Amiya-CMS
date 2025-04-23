# The FastAPI stuff~

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from app.crud import get_page_by_slug, list_pages
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin_route, aina_route, aiconfig_route, media_route, login_route,setup_route
from app.generator import generate_markdown_page
from fastapi.templating import Jinja2Templates
from app.auth import Depends,get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.auth import secrets_file_exists

app = FastAPI(
    title="AmiyaCMS",
    description="A cute tiny little CMS for smol projects",
    version="0.1.0",
)

@app.middleware("http")
async def check_setup_middleware(request: Request, call_next):
    # Skip setup check for these paths
    if request.url.path in ['/setup', '/check-setup', '/static', '/login']:
        return await call_next(request)
    
    # Redirect to setup if no admin account exists
    if not secrets_file_exists() and request.url.path != '/setup':
        return RedirectResponse(url='/setup')
    
    return await call_next(request)

templates = Jinja2Templates(directory="templates")

# Public Routers
app.include_router(setup_route.router)
app.include_router(media_route.router)
app.include_router(login_route.router)

# Protected Routers
app.include_router(
    admin_route.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    aiconfig_route.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    aina_route.router,
    dependencies=[Depends(get_current_user)]
)


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
    if page.html != None and page.html != "":
        return HTMLResponse(content=page.html, status_code=200)
    else:
        generated = generate_markdown_page(page.title,page.markdown)
        return HTMLResponse(content=generated, status_code=200)

# Just in case someone want to add SPA functionality
@app.get("/api/site/{slug}")
async def api_site(slug: str):
    page = get_page_by_slug(slug)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page.__dict__

