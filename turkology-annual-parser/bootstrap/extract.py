from typing import List, Set

from domain.citation import Citation


def extract_known_authors(citations: List[Citation]) -> Set[str]:
    known_authors = set()
    for citation in citations:
        for author in citation.authors:
            if author.raw:
                known_authors.add(author.raw)
    known_authors.update(HARDCODED_AUTHORS)
    return known_authors


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
