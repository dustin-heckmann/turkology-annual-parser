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
            reference = citation.ta_references[0]
            repetitions_by_citation[(reference['volume'], reference['number'])].append(citation)
    return repetitions_by_citation


def add_repeated_info_to_citations(citations, repetitions_by_citation) -> List[Citation]:
    updated_citations = []
    repetitions = set()
    for citation in citations:
        citation_key = (citation.volume, citation.number)
        current_repetitions = repetitions_by_citation.get(citation_key, [])
        repetitions.update(
            {(repetition.volume, repetition.number) for repetition in current_repetitions}
        )
        citation = add_repeated_info_to_citation(
            citation,
            current_repetitions
        )
        if citation_key in repetitions:
            citation = replace(citation, type=CitationType.REPETITION)
        updated_citations.append(citation)
    return updated_citations


def add_repeated_info_to_citation(citation, repetitions):
    for repetition in repetitions:
        citation = replace(
            citation,
            comments=citation.comments + repetition.comments,
            amendments=citation.amendments + repetition.amendments,
            reviews=citation.reviews + repetition.reviews,
        )
    return citation
