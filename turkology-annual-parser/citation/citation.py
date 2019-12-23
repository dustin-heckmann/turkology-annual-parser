from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


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
    id: str = None
    volume: str = None
    number: int = None
    type: CitationType = None
    title: str = None
    authors: List[Person] = field(default_factory=list)
    editors: List[Person] = field(default_factory=list)
    translators: List[Person] = field(default_factory=list)
    keywords: List[dict] = field(default_factory=list)
    comments: List[str] = None
    reviews: List[str] = None
    _meta: dict = field(default_factory=dict)
    raw_text: str = ''
    published_in: dict = None
    number_of_pages: str = None
    number_of_volumes: str = None
    location: str = None
    material: List[dict] = field(default_factory=list)
    amendments: List[str] = field(default_factory=list)
    date_published: dict = field(default_factory=dict)
    originalIndex: int = None
    type: Optional[str] = None
    ta_references: List[dict] = field(default_factory=list)
    page_start: int = None
    page_end: int = None
    series: str = None
    date: dict = None
    remaining_text: str = None
    fully_parsed: bool = None

    @classmethod
    def from_json(cls, citation_json: dict):
        return Citation(
            id=citation_json['_id'],
            volume=citation_json['volume'],
            number=citation_json['number'],
            type=citation_json['type'],
            title=citation_json['title'],
            authors=[Person(**author) for author in citation_json['authors']],
            editors=[Person(**editor) for editor in citation_json['editors']],
            translators=[Person(**translator) for translator in citation_json['translators']],
            keywords=citation_json['keywords'],
            comments=citation_json['comments'],
            reviews=citation_json['reviews'],
            raw_text=citation_json['rawText'],
            published_in=citation_json['publishedIn'],
            number_of_pages=citation_json['numberOfPages'],
            number_of_volumes=citation_json['numberOfVolumes'],
            location=citation_json['location'],
            material=citation_json['material'],
            amendments=citation_json['amendments'],
            date_published=citation_json['datePublished'],
            ta_references=citation_json['taReferences'],
            page_start=citation_json['pageStart'],
            page_end=citation_json['pageEnd'],
            series=citation_json['series'],
            date=citation_json['date']
        )
