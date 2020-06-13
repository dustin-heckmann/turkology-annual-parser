from collections import defaultdict
from dataclasses import replace
from typing import Iterable, List, Dict, Tuple

from domain.citation import Citation, CitationType


def resolve_repetitions(citations: Iterable[Citation]):
    citations = list(citations)
    repetitions_by_citation = gather_repetitions_by_citations(citations)
    return add_repeated_info_to_citations(citations, repetitions_by_citation)


def gather_repetitions_by_citations(
        citations: List[Citation]
) -> Dict[Tuple[int, int], List[Citation]]:
    repetitions_by_citation = defaultdict(list)
    for citation in citations:
        if citation.ta_references:
            citation = replace(citation, type=CitationType.REPETITION)
            reference = citation.ta_references[0]
            repetitions_by_citation[(reference['volume'], reference['number'])].append(citation)
    return repetitions_by_citation


def add_repeated_info_to_citations(citations, repetitions_by_citation) -> List[Citation]:
    citations = list(citations)
    for citation in citations:
        citation_key = (citation.volume, citation.number)
        for repetition in repetitions_by_citation.get(citation_key, []):
            for extension_field in ('comments', 'amendments', 'reviews'):
                if getattr(repetition, extension_field):
                    getattr(citation, extension_field).extend(
                        getattr(repetition, extension_field)
                    )
    return citations
