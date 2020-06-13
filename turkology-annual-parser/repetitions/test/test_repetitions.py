from domain.citation import Citation, CitationType
from ..repetitions import resolve_repetitions


def test_sets_citation_type_to_repetition():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(volume=2, number=1, ta_references=[{"volume": 1, "number": 1}]),
    ]

    # when
    actual_citations = resolve_repetitions(citations)

    # then
    assert actual_citations[1].type == CitationType.REPETITION


def test_adds_comments_from_repetition():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(
            volume=2,
            number=1,
            ta_references=[{"volume": 1, "number": 1}],
            comments=['A comment']
        ),
    ]

    # when
    actual_citations = resolve_repetitions(citations)

    # then
    assert actual_citations[0].comments == ['A comment']


def test_adds_amendments_from_repetition():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(
            volume=2,
            number=1,
            ta_references=[{"volume": 1, "number": 1}],
            amendments=['An amendment']
        ),
    ]

    # when
    actual_citations = resolve_repetitions(citations)

    # then
    assert actual_citations[0].amendments == ['An amendment']


def test_adds_reviews_from_repetition():
    # given
    citations = [
        Citation(volume=1, number=1),
        Citation(
            volume=2,
            number=1,
            ta_references=[{"volume": 1, "number": 1}],
            reviews=['A review']
        ),
    ]

    # when
    actual_citations = resolve_repetitions(citations)

    # then
    assert actual_citations[0].reviews == ['A review']
