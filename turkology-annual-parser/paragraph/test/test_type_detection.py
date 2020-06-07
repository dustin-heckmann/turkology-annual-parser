from domain.paragraph import Paragraph, ParagraphType
from ..type_detection import detect_paragraph_types

KEYWORD_MAPPING = {
    'A': {'de': 'Allgemeines'},
    'AC': {'de': 'Bibliotheken'},
}


def test_detect_paragraph_types():
    sample_paragraphs_with_expected_types = [
        ('Something', None),
        ('ZEITSCHRIFTEN  UND', ParagraphType.JOURNAL_SECTION_BEGIN),
        ('Something', None),
        ('A. Allgemeines', ParagraphType.KEYWORD),
        ('1. First citation', ParagraphType.CITATION),
        ('• Some bullet point', ParagraphType.AMENDMENT),
        ('3. Second citation', ParagraphType.CITATION),
        ('Ac. bibliotheken', ParagraphType.KEYWORD),
        ('4. Third citation', ParagraphType.CITATION),
        ('Autoren, Herausgeber, Übersetzer, Rezensenten', ParagraphType.AUTHOR_INDEX_BEGIN),
        ('Something', None),
    ]
    paragraphs = [Paragraph(text=p, volume='130') for p, _ in sample_paragraphs_with_expected_types]
    paragraphs = list(detect_paragraph_types(paragraphs, KEYWORD_MAPPING))
    detected_types = [p.type for p in paragraphs]
    assert detected_types == [paragraph_type for _, paragraph_type in sample_paragraphs_with_expected_types]
