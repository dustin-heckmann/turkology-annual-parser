from paragraph.type_detection import detect_paragraph_types

KEYWORD_MAPPING = {
    'A': ['Allgemeines', ''],
    'AC': ['Bibliotheken', ''],
}


def test_detect_paragraph_types():
    sample_paragraphs_with_expected_types = [
        ('Something', None),
        ('ZEITSCHRIFTEN  UND', 'journal-section-begin'),
        ('Something', None),
        ('A. Allgemeines', 'keyword'),
        ('1. First citation', 'citation'),
        ('• Some bullet point', 'amendment'),
        ('3. Second citation', 'citation'),
        ('Ac. bibliotheken', 'keyword'),
        ('4. Third citation', 'citation'),
        ('Autoren, Herausgeber, Übersetzer, Rezensenten', 'author-index-begin'),
        ('Something', None),
    ]
    paragraphs = [{'text': p, 'volume': '130'} for p, _ in sample_paragraphs_with_expected_types]
    paragraphs = list(detect_paragraph_types(paragraphs, KEYWORD_MAPPING))
    detected_types = [p['type'] for p in paragraphs]
    assert detected_types == [paragraph_type for _, paragraph_type in sample_paragraphs_with_expected_types]
