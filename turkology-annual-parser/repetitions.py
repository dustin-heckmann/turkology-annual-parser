from collections import defaultdict


def add_repeated_info(citations):
    repetition_links = defaultdict(list)
    for citation in citations:
        if citation.get('taReferences', []):
            citation['type'] = 'repetition'
            citation['_added_repetition'] = True
            reference = citation['taReferences'][0]
            repetition_links[(reference['volume'], reference['number'])].append(citation)

    for citation in citations:
        citation_key = (citation['volume'], citation['number'])
        for repetition in repetition_links.get(citation_key, []):
            for extension_field in ('comments', 'amendments', 'reviews'):
                if repetition.get(extension_field, []):
                    citation.setdefault(extension_field, []).extend(repetition[extension_field])
                    citation['_added_repetition'] = True
