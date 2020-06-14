from typing import List, Set

from domain.citation import Citation


def extract_known_authors(citations: List[Citation]) -> Set[str]:
    known_authors = set()
    for citation in citations:
        for author in citation.authors:
            if author.raw:
                known_authors.add(author.raw)
    return known_authors
