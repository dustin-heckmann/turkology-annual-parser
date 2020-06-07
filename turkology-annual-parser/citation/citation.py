import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class CitationType(Enum):
    ARTICLE = 'article'
    COLLECTION = 'collection'
    MONOGRAPH = 'monograph'
    REPETITION = 'repetition'
    CONFERENCE = 'conference'


@dataclass
class Person:
    first: Optional[str] = None
    middle: Optional[str] = None
    last: Optional[str] = None
    raw: Optional[str] = None


@dataclass
class Citation:
    id: Optional[str] = None
    volume: Optional[int] = None
    number: Optional[int] = None
    type: CitationType = None
    title: Optional[str] = None
    authors: List[Person] = field(default_factory=list)
    editors: List[Person] = field(default_factory=list)
    translators: List[Person] = field(default_factory=list)
    keywords: List[dict] = field(default_factory=list)
    comments: List[str] = None
    reviews: List[str] = None
    raw_text: str = ''
    published_in: dict = None
    number_of_pages: Optional[str] = None
    number_of_volumes: Optional[str] = None
    location: Optional[str] = None
    material: List[dict] = field(default_factory=list)
    amendments: List[str] = field(default_factory=list)
    date_published: dict = None
    originalIndex: Optional[int] = None
    ta_references: List[dict] = field(default_factory=list)
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    series: Optional[str] = None
    date: dict = None
    remaining_text: Optional[str] = None

    def fully_parsed(self) -> bool:
        fully_parsed_pattern = re.compile(r'({{{\s*[\w_]+\s*}}}[., ]*)+')
        return fully_parsed_pattern.fullmatch(self.remaining_text) is not None
