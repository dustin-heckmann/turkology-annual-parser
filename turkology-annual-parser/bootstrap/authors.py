import logging
import re
from dataclasses import replace
from typing import List, Iterable, Optional, Set

import regex

from citation.citation_parsing import reparse_citation
from citation.field_parsing import parse_name
from domain.citation import Citation


def reparse_citations_using_known_authors(citations: List[Citation]):
    authors = extract_known_authors_pattern(citations)
    authors.update(HARDCODED_AUTHORS)
    logging.debug('Found {} distinct authors'.format(len(authors)))
    return insert_known_authors(citations, authors)


def extract_known_authors_pattern(citations: List[Citation]) -> Set[str]:
    known_authors = set()
    for citation in citations:
        for author in citation.authors:
            if author.raw:
                known_authors.add(author.raw)
    return known_authors


def insert_known_authors(
        citations: List[Citation],
        known_authors: Iterable[str]
) -> Iterable[Citation]:
    known_authors_pattern = '|'.join(
        [re.escape(author.strip().lower()) for author in known_authors])
    for citation in citations:
        if not citation.fully_parsed() and not citation.authors:
            citation_with_authors = (
                    find_multiple_authors(citation, known_authors_pattern)
                    or find_single_author(citation, known_authors_pattern)
            )
            if citation_with_authors:
                citation = reparse_citation(citation_with_authors)
        yield citation


def find_multiple_authors(citation: Citation, known_authors_pattern) -> Optional[Citation]:
    multiple_authors_pattern = regex.compile(
        f'^({known_authors_pattern}){{e<=1}}(?: +(?:—|-) '
        fr'+({known_authors_pattern}){{e<=1}})+\.?\s+(\p{{Lu}}[^ .]+ .+)',
        regex.UNICODE | regex.IGNORECASE | regex.DOTALL
    )
    authors_match = multiple_authors_pattern.findall(citation.remaining_text)
    if not authors_match:
        return None
    authors_match = authors_match[0]
    author_names = [name for name in authors_match[:-1] if name]
    remaining_text = '{{{ authors }}} ' + authors_match[-1]
    return replace(
        citation,
        remaining_text=remaining_text,
        authors=[parse_name(name) for name in author_names]
    )


def find_single_author(citation: Citation, known_authors_pattern) -> Optional[Citation]:
    authors_pattern = regex.compile(
        r'^({}){{e<=1}}\.?\s+(\p{{Lu}}[^ .]+ )'.format(known_authors_pattern),
        regex.UNICODE | regex.IGNORECASE
    )
    author_match = authors_pattern.search(citation.remaining_text)

    if not author_match:
        return None
    author_name = author_match.group(1)
    remaining_text = '{{{ authors }}} ' + citation.remaining_text[author_match.span(2)[0]:]
    return replace(
        citation,
        remaining_text=remaining_text,
        authors=[parse_name(author_name)]
    )


HARDCODED_AUTHORS = {
    'Condurachi, Em',
    'Kakük, Z',
    'Yoman, Yakut',
    'Kobeneva, T. A',
    'Djukanovic, Marija',
    'Zagorka Janc',
    'Sohbweide, Hanna',
    'Tübkay, Cevdet',
    'Eren, ismail',
    'Baysal,   Jale',
    'Spiridonakis, B. G',
    'Uçankuş, Hasan T',
    'Landau, Jacob M',
    'Özeğe, Seyfettin',
}
