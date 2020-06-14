from domain.citation import Citation, Person
from ..extract import extract_known_authors


def test_extracts_single_author_from_one_citation():
    # given
    citations = [Citation(authors=[Person(raw='Smith, Jordan')])]

    # when
    known_authors = extract_known_authors(citations)

    # then
    assert known_authors == {'Smith, Jordan'}


def test_extracts_multiple_authors_from_one_citation():
    # given
    citations = [Citation(authors=[Person(raw='Ozkut Korkmaz'), Person(raw='Smith, Jordan')])]

    # when
    known_authors = extract_known_authors(citations)

    # then
    assert known_authors == {'Ozkut Korkmaz', 'Smith, Jordan'}


def test_extracts_authors_from_multiple_citations():
    # given
    citations = [
        Citation(authors=[Person(raw='Ozkut Korkmaz')]),
        Citation(authors=[Person(raw='Smith, Jordan')]),
    ]

    # when
    known_authors = extract_known_authors(citations)

    # then
    assert known_authors == {'Ozkut Korkmaz', 'Smith, Jordan'}


def test_extracts_nothing_if_no_authors_present():
    # given
    citations = [Citation(authors=[])]

    # when
    known_authors = extract_known_authors(citations)

    # then
    assert len(known_authors) == 0


def test_extracts_nothing_if_no_citations_present():
    # given
    citations = []

    # when
    known_authors = extract_known_authors(citations)

    # then
    assert len(known_authors) == 0
