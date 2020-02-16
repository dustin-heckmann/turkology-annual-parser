import re
from dataclasses import dataclass, field
from typing import List

from citation.citation import CitationType


@dataclass
class IntermediateCitation:
    volume: int = None
    number: str = None
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
    type: CitationType = None
    ta_references: List[str] = field(default_factory=list)
    page_range: str = None
    series: str = None
    remaining_text: str = None
    page_start: str = None
    page_end: str = None
    raw_text: str = None

    @property
    def fully_parsed(self) -> bool:
        fully_parsed_pattern = re.compile(r'({{{\s*[\w_]+\s*}}}[., ]*)+')
        return fully_parsed_pattern.fullmatch(self.remaining_text) is not None
