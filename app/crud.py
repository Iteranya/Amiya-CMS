import re
from typing import List, Optional
from tinydb import where
from app.db import db, SiteQuery, flush_db
from app.models import Page, Image
from pydantic import TypeAdapter

# Save a Page to the DB
def is_slug_friendly(slug: str) -> bool:
    return re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) is not None

def create_page(page: Page) -> int:
    if not is_slug_friendly(page.slug):
        print("error caught")
        raise ValueError(f"Invalid slug format: '{page.slug}'. Slugs must be lowercase alphanumeric with hyphens.")
    
    # Check for duplicate slug - assuming db is a TinyDB instance
    # Replace this line:
    # if db.contains({'slug': page.slug}):
    
    # With this (using TinyDB Query):
    if db.contains(SiteQuery.slug == page.slug):
        print("error caught")
        raise ValueError(f"Slug '{page.slug}' already exists.")

    data = page.__dict__
    doc_id = db.insert(data)
    flush_db()  # Ensure data is written to disk
    return doc_id

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
    result = db.remove(SiteQuery.slug == slug)
    flush_db()  # Ensure data is written to disk
    return result

# Update a Page by slug, make new if don't exist
def update_page(slug: str, updated_data: dict) -> bool:
    # Try to find the document with the given slug
    existing_doc = db.get(SiteQuery.slug == slug)
    
    if existing_doc:
        # Document exists, update it
        result = db.update(updated_data, SiteQuery.slug == slug)
        flush_db()
        return bool(result)
    else:
        # Document doesn't exist, create it
        # Make sure the slug is included in the data
        new_data = updated_data.copy()
        new_data['slug'] = slug
        db.insert(new_data)
        flush_db()
        return True