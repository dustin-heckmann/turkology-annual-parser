# -*- coding: utf-8 -*-

from typing import Iterator

from citation.intermediate_citation import IntermediateCitation
from paragraph.paragraph import Paragraph, ParagraphType


def assemble_citations(paragraphs: Iterator[Paragraph]):
    current_keyword = None
    current_citation = None

    for paragraph in paragraphs:
        if paragraph.type == ParagraphType.KEYWORD:
            current_keyword = paragraph.text
        elif paragraph.type == ParagraphType.CITATION:
            if current_citation:
                yield current_citation
            current_citation = IntermediateCitation(
                volume=paragraph.volume,
                raw_text=paragraph.text,
                keywords=[current_keyword] if current_keyword else [],
            )
        elif paragraph.type == ParagraphType.AMENDMENT:
            current_citation.amendments.append(paragraph.text)
    if current_citation:
        yield current_citation
