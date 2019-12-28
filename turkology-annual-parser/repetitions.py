from collections import defaultdict
from typing import List

from citation.citation import Citation, CitationType


def add_repeated_info(citations: List[Citation]):
    citations = list(citations)
    repetition_links = defaultdict(list)
    for citation in citations:
        if citation.ta_references:
            citation.type = CitationType.REPETITION
            reference = citation.ta_references[0]
            repetition_links[(reference['volume'], reference['number'])].append(citation)
    for citation in citations:
        citation_key = (citation.volume, citation.number)
        for repetition in repetition_links.get(citation_key, []):
            for extension_field in ('comments', 'amendments', 'reviews'):
                if getattr(repetition, extension_field):
                    getattr(citation, extension_field).extend(
                        getattr(repetition, extension_field))
    return citations
