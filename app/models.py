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
    url: str
    content: str
    content_length: int
    markdown: str
    images: List[Image]
    html: str
    slug: str