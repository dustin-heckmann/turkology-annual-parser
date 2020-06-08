from collections import defaultdict, Counter
from dataclasses import replace
from typing import Iterator, DefaultDict

from domain.citation import Citation


def assign_citation_ids(citations: Iterator[Citation]):
    volume_numbers: DefaultDict[int, Counter] = defaultdict(Counter)

    for citation in citations:
        citation_id = f'{citation.volume}-{citation.number}'
        previous_occurrences = volume_numbers[citation.volume][citation.number]
        if previous_occurrences:
            citation_id += f'-{previous_occurrences}'
        volume_numbers[citation.volume][citation.number] += 1
        yield replace(citation, id=citation_id)
