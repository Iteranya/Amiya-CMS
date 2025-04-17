from pydantic.dataclasses import dataclass
from typing import List, Optional

@dataclass
class Image:
    image: str
    thumbnail: str
    url: str
    height: int
    width: int
    source: str
    title: Optional[str] = None

@dataclass
class Page:
    title: str
    content: str
    markdown: str
    html: str
    slug: str
    url: Optional[str] = None
    content_length: Optional[int] = None
    tags: Optional[List[Image]] = None
    images: Optional[List[Image]] = None