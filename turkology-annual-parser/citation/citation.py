from dataclasses import dataclass, field
from enum import Enum
from typing import List


class CitationType(Enum):
    ARTICLE = 'article'
    COLLECTION = 'collection'
    MONOGRAPH = 'monograph'
    REPETITION = 'repetition'
    CONFERENCE = 'conference'


@dataclass
class Person:
    first: str = None
    middle: str = None
    last: str = None
    raw: str = None


@dataclass
class Citation:
    volume: int = None
    number: int = None
    type: CitationType = None
    title: str = None
    authors: List[Person] = field(default_factory=list)
    editors: List[Person] = field(default_factory=list)
    translators: List[Person] = field(default_factory=list)
    keywords: List[dict] = field(default_factory=list)
    comments: List[str] = None
    reviews: List[str] = None
    raw_text: str = ''
    published_in: dict = None
    number_of_pages: str = None
    number_of_volumes: str = None
    location: str = None
    material: List[dict] = field(default_factory=list)
    amendments: List[str] = field(default_factory=list)
    date_published: dict = field(default_factory=dict)
    originalIndex: int = None
    ta_references: List[dict] = field(default_factory=list)
    page_start: int = None
    page_end: int = None
    series: str = None
    date: dict = None
    remaining_text: str = None
    fully_parsed: bool = None
