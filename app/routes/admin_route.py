from pathlib import Path
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from app.models import Page
from app.crud import create_page, delete_page, update_page, get_page_by_slug, list_pages
from pydantic import ValidationError
from app.bundler import StaticBundler

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/", response_class=HTMLResponse)

async def get_html():
    bundler = StaticBundler(
    template_path="static/admin-panel/index.html",
    scripts_dir="static/admin-panel/scripts",
    styles_dir="static/admin-panel/styles"
    )
    return bundler.generate_html()


# Add a new page
@router.post("/add", response_model=Dict)
async def add_page(page: Page):
    print("--------------ADD PAGE--------------")
    try:
        page_id = create_page(page)
        return {"message": "Page created successfully", "id": page_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete a page by slug
@router.delete("/delete/{slug}")
async def remove_page(slug: str):
    deleted = delete_page(slug)
    if deleted:
        return {"message": f"Page '{slug}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Page not found")


# Update a page by slug
@router.put("/update/{slug}")
async def edit_page(slug: str, updated_fields: dict):
    existing = get_page_by_slug(slug)
    if not existing:
        raise HTTPException(status_code=404, detail="Page not found")
    success = update_page(slug, updated_fields)
    return {"message": f"Page '{slug}' updated successfully"} if success else {"message": "No update performed"}


# List all pages for admin
@router.get("/list")
async def admin_list_pages():
    pages = list_pages()
    return [p.__dict__ for p in pages]
