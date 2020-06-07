import re
from typing import List, Optional

from dataclasses import dataclass, field

from domain.citation import CitationType


@dataclass
class IntermediateCitation:
    volume: Optional[int] = None
    number: Optional[str] = None
    title: Optional[str] = None
    authors: Optional[str] = None
    editors: Optional[str] = None
    translators: Optional[str] = None
    date: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    comment: Optional[str] = None
    published_in: Optional[str] = None
    number_of_pages: Optional[str] = None
    number_of_volumes: Optional[str] = None
    reviews: Optional[str] = None
    abstract_in: Optional[str] = None
    location: Optional[str] = None
    material: List[str] = field(default_factory=list)
    amendments: List[str] = field(default_factory=list)
    date_published: Optional[str] = None
    type: Optional[CitationType] = None
    ta_references: List[str] = field(default_factory=list)
    page_range: Optional[str] = None
    series: Optional[str] = None
    remaining_text: str = ''
    page_start: Optional[str] = None
    page_end: Optional[str] = None
    raw_text: str = ''

    @property
    def fully_parsed(self) -> bool:
        fully_parsed_pattern = re.compile(r'({{{\s*[\w_]+\s*}}}[., ]*)+')
        return fully_parsed_pattern.fullmatch(self.remaining_text) is not None
