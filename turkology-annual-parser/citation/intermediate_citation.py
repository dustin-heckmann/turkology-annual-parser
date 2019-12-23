from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class IntermediateCitation:
    volume: str = None
    number: str = None
    type: str = None
    title: str = None
    authors: str = None
    editors: str = None
    translators: str = None
    date: str = None
    keywords: List[str] = field(default_factory=list)
    comment: str = None
    published_in: str = None
    number_of_pages: str = None
    number_of_volumes: str = None
    reviews: str = None
    abstract_in: str = None
    location: str = None
    material: List[str] = field(default_factory=list)
    amendments: List[str] = field(default_factory=list)
    date_published: str = None
    type: Optional[str] = None
    ta_references: List[str] = field(default_factory=list)
    page_range: str = None
    series: str = None
    remaining_text: str = None
    page_start: str = None
    page_end: str = None
    fully_parsed: bool = False
    raw_text: str = None
