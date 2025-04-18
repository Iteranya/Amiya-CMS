from pydantic.dataclasses import dataclass
from typing import List, Optional

@dataclass
class Image:
    image: Optional[str] = None
    thumbnail: Optional[str] = None
    url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None
    source: Optional[str] = None
    title: Optional[str] = None

@dataclass
class Page:
    title: str
    slug: str
    content: Optional[str] = None
    markdown: Optional[str] = None
    html: Optional[str] = None
    url: Optional[str] = None
    content_length: Optional[int] = None
    tags: Optional[List[str]] = None
    images: Optional[List[Image]] = None