from domain.citation import Citation
from ..keywords import normalize_keywords_for_citation


def test_normalize_keywords():
    citation = Citation(
        keywords=[{'raw': 'A. ASDFERAWER'}]
    )
    keyword_mapping = {
        'A': {'de': 'Allgemeines', 'en': 'General'}
    }
    citation = normalize_keywords_for_citation(citation, keyword_mapping)
    assert citation.keywords == [
        {
            'code': 'A',
            'nameDE': 'Allgemeines',
            'nameEN': 'General',
            'raw': 'A. ASDFERAWER',
            'super': None
        }
    ]


def test_normalize_keywords_with_super_keyword():
    citation = Citation(
        keywords=[{'raw': 'AB. IRGENDWAS'}]
    )
    keyword_mapping = {
        'A': {'de': 'Allgemeines', 'en': 'General'},
        'AB': {'de': 'Spezielles', 'en': 'Specific'}
    }
    citation = normalize_keywords_for_citation(citation, keyword_mapping)
    assert citation.keywords == [
        {
            'code': 'AB',
            'nameDE': 'Spezielles',
            'nameEN': 'Specific',
            'raw': 'AB. IRGENDWAS',
            'super': {
                'code': 'A',
                'nameDE': 'Allgemeines',
                'nameEN': 'General',
                'raw': None,
                'super': None
            }
        }
    ]
