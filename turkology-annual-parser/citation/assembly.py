# -*- coding: utf-8 -*-

from collections import OrderedDict
from datetime import datetime
from typing import List

from paragraph.paragraph import Paragraph


def assemble_citations(paragraphs: List[Paragraph]):
    current_keyword = None
    current_citation = None

    for paragraph in paragraphs:
        if paragraph.type == 'keyword':
            current_keyword = paragraph.text
        elif paragraph.type == 'citation':
            if current_citation:
                yield current_citation
            current_citation = OrderedDict(
                volume=paragraph.volume,
                keywords=[current_keyword] if current_keyword else [],
                rawText=paragraph.text,
                _version=1,
                _last_modified=datetime.now(),
                _creator='<initial>',
            )
        elif paragraph.type == 'amendment':
            current_citation.setdefault('amendments', []).append(paragraph.text)
    if current_citation:
        yield current_citation
