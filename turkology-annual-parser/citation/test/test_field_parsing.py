from citation.citation import Citation, Person
from citation.field_parsing import parse_citation_fields
from citation.intermediate_citation import IntermediateCitation

CITATION = IntermediateCitation(
    fully_parsed=True,
    remaining_text='{{{ title }}}.  {{{ editors }}}   {{{ number_of_volumes }}} '
                   '{{{ location }}} {{{ date_published }}}{{{ series }}}.',
    raw_text='1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans '
             'Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, '
             '200/1-3).',
    series='Urban-Taschenbücher, 200/1-3',
    editors='Klaus Kreiser, Werner Diem, Hans Georg Majer',
    location='Stuttgart',
    authors='Bazin, L.',
    number='1',
    keywords=['A', 'B'],
    number_of_volumes='3',
    title='Lexikon der islamischen Welt',
    date_published='1974',
    type='collection',
    volume='1',
)


def test_parse_citation_fields():
    field_parsed_citation = parse_citation_fields(CITATION)

    assert field_parsed_citation == Citation(
        volume='1',
        number=1,
        type='collection',
        title='Lexikon der islamischen Welt',
        editors=[
            Person(first='Klaus', last='Kreiser', raw='Klaus Kreiser'),
            Person(first='Werner', last='Diem', raw='Werner Diem'),
            Person(first='Hans', middle='Georg', last='Majer', raw='Hans Georg Majer')
        ],
        keywords=['A', 'B'],
        reviews=[],
        comments=[],
        date_published={'year': 1974},
        location='Stuttgart',
        series='Urban-Taschenbücher, 200/1-3',
        number_of_volumes='3',
        authors=[
            Person(first='L.', last='Bazin', raw='Bazin, L.')
        ],
        raw_text='1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, 200/1-3).',
        remaining_text='{{{ title }}}.  {{{ editors }}}   {{{ number_of_volumes }}} {{{ location }}} {{{ date_published }}}{{{ series }}}.'
    )
