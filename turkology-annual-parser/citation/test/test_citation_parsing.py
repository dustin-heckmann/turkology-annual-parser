from citation.citation_parsing import CitationParser


def test_parse_citation():
    citation = {
        'volume': '1',
        'rawText': '1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, 200/1-3).',

    }
    parser = CitationParser()
    parsed_citation = parser.parse_citation(citation)
    assert parsed_citation == {
        'datePublished': '1974',
        'editors': [
            {
                'first': 'Klaus',
                'last': 'Kreiser',
                'raw': 'Klaus Kreiser'
            },
            {
                'first': 'Werner',
                'last': 'Diem',
                'raw': ' Werner Diem'
            },
            {
                'first': 'Hans',
                'last': 'Majer',
                'middle': 'Georg',
                'raw': ' Hans Georg Majer'
            }
        ],
        'fullyParsed': True,
        'location': 'Stuttgart',
        'number': 1,
        'numberOfVolumes': 3,
        'rawText': '1. Lexikon der islamischen Welt. Klaus Kreiser, Werner Diem, Hans '
                   'Georg Majer ed. 3 Bde., Stuttgart, 1974 (Urban-Taschenbücher, '
                   '200/1-3).',
        'remainingText': '{{{ title }}}.  {{{ editors }}}   {{{ numberOfVolumes }}} '
                         '{{{ location }}} {{{ datePublished }}}{{{ series }}}.',
        'series': 'Urban-Taschenbücher, 200/1-3',
        'title': 'Lexikon der islamischen Welt',
        'type': 'collection',
        'volume': '1'
    }
