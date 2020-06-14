import logging
import multiprocessing
import re
from dataclasses import replace
from multiprocessing.queues import Queue
from typing import List, Iterable, Optional

import regex

from citation.citation_parsing import reparse_citation
from citation.field_parsing import parse_name
from domain.citation import Citation
from .extract import extract_known_authors


def reparse_citations_using_known_authors(citations: List[Citation]):
    authors = extract_known_authors(citations)
    logging.debug('Found {} distinct authors'.format(len(authors)))

    queue = multiprocessing.Manager().Queue()
    chunks = split_into_chunks(
        filter(lambda c: not c.authors and not c.fully_parsed(), citations),
        int(len(citations) / multiprocessing.cpu_count())
    )
    with multiprocessing.Pool() as pool:
        args = ((chunk, authors, queue) for chunk in chunks)
        pool.starmap(insert_known_authors, args)
    pool.join()
    updated_citations = {}
    while not queue.empty():
        citation = queue.get()
        updated_citations[citation.id] = citation
    pool.close()
    logging.info(f'Found known authors in {len(updated_citations)} citations')
    return [
        updated_citations.get(citation.id, citation) for citation in citations
    ]


def split_into_chunks(items: Iterable[Citation], chunk_size: int):
    current_chunk = []
    for item in items:
        current_chunk.append(item)
        if len(current_chunk) == chunk_size:
            yield current_chunk
            current_chunk = []
    if current_chunk:
        yield current_chunk


def insert_known_authors(
        citations: List[Citation],
        known_authors: Iterable[str],
        queue: Queue
) -> None:
    known_authors_pattern = '|'.join(
        [re.escape(author.strip().lower()) for author in known_authors])

    multiple_authors_pattern = regex.compile(
        f'^({known_authors_pattern}){{e<=1}}(?: +(?:—|-) '
        fr'+({known_authors_pattern}){{e<=1}})+\.?\s+(\p{{Lu}}[^ .]+ .+)',
        regex.UNICODE | regex.IGNORECASE | regex.DOTALL
    )

    single_author_pattern = regex.compile(
        r'^({}){{e<=1}}\.?\s+(\p{{Lu}}[^ .]+ )'.format(known_authors_pattern),
        regex.UNICODE | regex.IGNORECASE
    )

    for citation in citations:
        citation_with_authors = (
                find_multiple_authors(citation, multiple_authors_pattern)
                or find_single_author(citation, single_author_pattern)
        )
        if citation_with_authors:
            queue.put(reparse_citation(citation_with_authors))


def find_multiple_authors(citation: Citation, multiple_authors_pattern) -> Optional[Citation]:
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


def find_single_author(citation: Citation, single_author_pattern) -> Optional[Citation]:
    author_match = single_author_pattern.search(citation.remaining_text)

    if not author_match:
        return None
    author_name = author_match.group(1)
    remaining_text = '{{{ authors }}} ' + citation.remaining_text[author_match.span(2)[0]:]
    return replace(
        citation,
        remaining_text=remaining_text,
        authors=[parse_name(author_name)]
    )
