from collections import OrderedDict
from datetime import datetime

from freezegun import freeze_time

from citation.assembly import assemble_citations
from paragraph.paragraph import Paragraph


def test_can_take_empty_paragraph_list():
    assert list(assemble_citations([])) == []


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation():
    paragraphs = [
        Paragraph(type='citation', volume='5', text='1. Some citation')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [OrderedDict([
        ('volume', '5'),
        ('keywords', []),
        ('rawText', '1. Some citation'),
        ('_version', 1),
        ('_last_modified',
         datetime(2023, 7, 14, 12, 0, 1)),
        ('_creator', '<initial>')
    ])]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation_with_keyword():
    paragraphs = [
        Paragraph(type='keyword', volume='5', text='A'),
        Paragraph(type='citation', volume='5', text='1. Some citation')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [OrderedDict([
        ('volume', '5'),
        ('keywords', ['A']),
        ('rawText', '1. Some citation'),
        ('_version', 1),
        ('_last_modified',
         datetime(2023, 7, 14, 12, 0, 1)),
        ('_creator', '<initial>')
    ])]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_one_citation_with_amendment():
    paragraphs = [
        Paragraph(type='citation', volume='5', text='1. Some citation'),
        Paragraph(type='amendment', volume='5', text='Some amendment')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [OrderedDict([
        ('volume', '5'),
        ('keywords', []),
        ('rawText', '1. Some citation'),
        ('_version', 1),
        ('_last_modified',
         datetime(2023, 7, 14, 12, 0, 1)),
        ('_creator', '<initial>'),
        ('amendments', ['Some amendment'])
    ])]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_two_citations_with_keywords():
    paragraphs = [
        Paragraph(type='keyword', volume='5', text='A'),
        Paragraph(type='citation', volume='5', text='1. Citation 1'),
        Paragraph(type='keyword', volume='5', text='B'),
        Paragraph(type='amendment', volume='5', text='Some amendment'),
        Paragraph(type='citation', volume='5', text='2. Citation 2')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        OrderedDict([
            ('volume', '5'),
            ('keywords', []),
            ('rawText', '1. Citation 1'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>'),
        ]),
        OrderedDict([
            ('volume', '5'),
            ('keywords', []),
            ('rawText', '2. Citation 2'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>')
        ])
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_three_citations():
    paragraphs = [
        Paragraph(type='citation', volume='5', text='1. Citation 1'),
        Paragraph(type='citation', volume='5', text='2. Citation 2'),
        Paragraph(type='citation', volume='5', text='3. Citation 3')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        OrderedDict([
            ('volume', '5'),
            ('keywords', []),
            ('rawText', '1. Citation 1'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>'),
        ]),
        OrderedDict([
            ('volume', '5'),
            ('keywords', []),
            ('rawText', '2. Citation 2'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>')
        ]),
        OrderedDict([
            ('volume', '5'),
            ('keywords', []),
            ('rawText', '3. Citation 3'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>')
        ])
    ]


@freeze_time("2023-07-14 12:00:01")
def test_assembles_two_citations_with_keywords():
    paragraphs = [
        Paragraph(type='keyword', volume='5', text='A'),
        Paragraph(type='citation', volume='5', text='1. Citation 1'),
        Paragraph(type='keyword', volume='5', text='B'),
        Paragraph(type='amendment', volume='5', text='Some amendment'),
        Paragraph(type='citation', volume='5', text='2. Citation 2')
    ]
    citations = list(assemble_citations(paragraphs))
    assert citations == [
        OrderedDict([
            ('volume', '5'),
            ('keywords', ['A']),
            ('rawText', '1. Citation 1'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>'),
            ('amendments', ['Some amendment'])
        ]),
        OrderedDict([
            ('volume', '5'),
            ('keywords', ['B']),
            ('rawText', '2. Citation 2'),
            ('_version', 1),
            ('_last_modified',
             datetime(2023, 7, 14, 12, 0, 1)),
            ('_creator', '<initial>')
        ])
    ]
