# -*- coding: utf-8 -*-
import logging
from typing import Iterable

from domain.intermediate_citation import IntermediateCitation
from domain.paragraph import Paragraph, ParagraphType


def assemble_citations(paragraphs: Iterable[Paragraph]):
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
            if current_citation:
                current_citation.amendments.append(paragraph.text)
            else:
                logging.warning(f'Found amendment before a citation. Skipping paragraph: {str(paragraph)}')

    if current_citation:
        yield current_citation
