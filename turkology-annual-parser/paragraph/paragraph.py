from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ParagraphType(Enum):
    KEYWORD = 'keyword'
    CITATION = 'citation'
    AMENDMENT = 'amendment'
    AUTHOR_INDEX_BEGIN = 'author-index-begin'
    JOURNAL = 'journal'
    JOURNAL_SECTION_BEGIN = 'journal-section-begin'


@dataclass
class Paragraph:
    volume: int = None
    text: str = None
    originalIndex: int = None
    type: Optional[ParagraphType] = None
