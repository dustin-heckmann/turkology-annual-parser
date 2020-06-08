from citation.id_assignment import assign_citation_ids
from domain.citation import Citation


def test_assign_unique():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(volume=1, number=2),
        Citation(volume=1, number=3),
    ]

    # when
    citations_with_ids = list(assign_citation_ids(citations))

    # then
    assert citations_with_ids == [
        Citation(volume=1, number=1, id='1-1'),
        Citation(volume=1, number=2, id='1-2'),
        Citation(volume=1, number=3, id='1-3'),
    ]


def test_assign_duplicate():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(volume=1, number=2),
        Citation(volume=1, number=1),
        Citation(volume=1, number=1),
    ]

    # when
    citations_with_ids = list(assign_citation_ids(citations))

    # then
    assert citations_with_ids == [
        Citation(volume=1, number=1, id='1-1'),
        Citation(volume=1, number=2, id='1-2'),
        Citation(volume=1, number=1, id='1-1-1'),
        Citation(volume=1, number=1, id='1-1-2'),
    ]
