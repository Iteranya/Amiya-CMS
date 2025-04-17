from typing import List, Optional
from tinydb import where
from app.db import db, SiteQuery
from app.models import Page, Image
from pydantic import TypeAdapter

# Save a Page to the DB
def create_page(page: Page) -> int:
    data = page.__dict__
    return db.insert(data)

def get_page_by_slug(slug: str) -> Optional[Page]:
    result = db.search(SiteQuery.slug == slug)
    if result:
        # Create a TypeAdapter for the Page model
        page_adapter = TypeAdapter(Page)
        # Use validate_python to parse the data
        return page_adapter.validate_python(result[0])
    return None

# List all Pages
def list_pages() -> List[Page]:
    results = db.all()
    page_adapter = TypeAdapter(List[Page])
    return page_adapter.validate_python(results)

# Delete a Page by slug
def delete_page(slug: str) -> int:
    return db.remove(SiteQuery.slug == slug)

# Update a Page by slug
def update_page(slug: str, updated_data: dict) -> bool:
    result = db.update(updated_data, SiteQuery.slug == slug)
    return bool(result)
