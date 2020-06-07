from freezegun import freeze_time

from domain.intermediate_citation import IntermediateCitation
from domain.paragraph import Paragraph, ParagraphType
from ..assembly import assemble_citations


def test_can_take_empty_paragraph_list():
    assert list(assemble_citations([])) == []


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation():
    paragraphs = [
        Paragraph(type=ParagraphType.CITATION, volume=5, text='1. Some citation')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        IntermediateCitation(
            volume=5,
            keywords=[],
            raw_text='1. Some citation'
        )
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation_with_keyword():
    paragraphs = [
        Paragraph(type=ParagraphType.KEYWORD, volume=5, text='A'),
        Paragraph(type=ParagraphType.CITATION, volume=5, text='1. Some citation')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        IntermediateCitation(
            volume=5,
            raw_text='1. Some citation',
            keywords=['A']
        )
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation_with_amendment():
    paragraphs = [
        Paragraph(type=ParagraphType.CITATION, volume=5, text='1. Some citation'),
        Paragraph(type=ParagraphType.AMENDMENT, volume=5, text='Some amendment')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        IntermediateCitation(
            volume=5,
            keywords=[],
            raw_text='1. Some citation',
            amendments=['Some amendment']
        )
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_three_citations():
    paragraphs = [
        Paragraph(type=ParagraphType.CITATION, volume=5, text='1. Citation 1'),
        Paragraph(type=ParagraphType.CITATION, volume=5, text='2. Citation 2'),
        Paragraph(type=ParagraphType.CITATION, volume=5, text='3. Citation 3')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        IntermediateCitation(
            volume=5,
            raw_text='1. Citation 1'
        ),
        IntermediateCitation(
            volume=5,
            raw_text='2. Citation 2',
        ),
        IntermediateCitation(
            volume=5,
            raw_text='3. Citation 3',
        )
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_two_citations_with_keywords():
    paragraphs = [
        Paragraph(type=ParagraphType.KEYWORD, volume=5, text='A'),
        Paragraph(type=ParagraphType.CITATION, volume=5, text='1. Citation 1'),
        Paragraph(type=ParagraphType.KEYWORD, volume=5, text='B'),
        Paragraph(type=ParagraphType.AMENDMENT, volume=5, text='Some amendment'),
        Paragraph(type=ParagraphType.CITATION, volume=5, text='2. Citation 2')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        IntermediateCitation(
            volume=5,
            raw_text='1. Citation 1',
            keywords=['A'],
            amendments=['Some amendment'],
        ),
        IntermediateCitation(
            volume=5,
            raw_text='2. Citation 2',
            keywords=['B'],
            amendments=[]
        )
    ]
