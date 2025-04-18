from typing import List, Optional
from fastapi import APIRouter, HTTPException, Form
from app.models import Page
from app.crud import create_page, delete_page, update_page, get_page_by_slug, list_pages
from pydantic import ValidationError

router = APIRouter(prefix="/admin", tags=["Admin"])



# Add a new page
@router.post("/add")
async def add_page(
    title: str = Form(...),
    content: str = Form(...),
    markdown: str = Form(...),
    tags: Optional[List[str]] = Form(...),
    html: str = Form(...),
    slug: str = Form(...)
):
    try:
        # Convert JSON string to Python list for images

        # Build Page object
        page = Page(
            title=title,
            content=content,
            markdown=markdown,
            html=html,
            tags= tags,
            slug=slug
        )
        page_id = create_page(page)
        return {"message": "Page created successfully", "id": page_id}
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
