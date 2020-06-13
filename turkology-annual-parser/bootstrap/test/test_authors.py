from bootstrap.authors import insert_known_authors
from citation.citation_parsing import parse_citation
from citation.field_parsing import parse_citation_fields
from domain.citation import Citation, CitationType, Person
from domain.intermediate_citation import IntermediateCitation


def test_insert_known_authors():
    raw_text = ''.join((
        '12. Handžić, Adem ',
        'Problematika sakupljanja i izdavanja turskih '
        'istorij-skih izvora u radu Orijentalnog Instituta. ',
        'In: POF 20-21.1970/71 (1974).213-221. ',
        '[Die Problematik der Erfassung und Herausgabe der türkischen historischen Quellen ',
        'im Rahmen der Arbeiten des Orientalischen Instituts in Sarajevo, Jugoslavien.]',
    ))
    raw_citation = IntermediateCitation(volume=1, raw_text=raw_text)
    parsed_citation = parse_citation_fields(parse_citation(raw_citation))
    [parsed_citation] = insert_known_authors([parsed_citation], ['Handžić, Adem'])

    assert parsed_citation == Citation(
        volume=1,
        number=12,
        type=CitationType.ARTICLE,
        authors=[Person(last='Handžić', first='Adem', raw='Handžić, Adem')],
        title='Problematika sakupljanja i izdavanja turskih '
              'istorij-skih izvora u radu Orijentalnog Instituta',
        comments=[
            'Die Problematik der Erfassung und Herausgabe der türkischen historischen Quellen '
            'im Rahmen der Arbeiten des Orientalischen Instituts in Sarajevo, Jugoslavien'
        ],
        reviews=[],
        raw_text=raw_text,
        published_in={
            'journal': 'POF',
            'volumeStart': 20,
            'volumeEnd': 21,
            'yearStart': 1970,
            'yearEnd': 1971,
            'yearParentheses': 1974,
            'pageStart': 213,
            'pageEnd': 221,
            'type': 'journal',
            'raw': 'POF 20-21.1970/71 (1974).213-221'
        },
        ta_references=[],
        remaining_text='{{{ authors }}} {{{ title }}} {{{ in }}}'
    )
