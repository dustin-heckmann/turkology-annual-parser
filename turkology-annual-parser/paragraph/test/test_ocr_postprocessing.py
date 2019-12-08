from paragraph.ocr_postprocessing import postprocess_paragraph

BULLET_POINT = '•'


def test_corrects_paragraph_with_leading_wrongly_detected_bullet_point():
    processed_paragraph = postprocess_paragraph({'text': 'φ Some text'})
    assert processed_paragraph == {'text': f'{BULLET_POINT} Some text', 'original_text': 'φ Some text'}


def test_does_not_change_paragraph_if_character_is_not_leading():
    paragraph = {'text': 'Some text φ and some more'}
    processed_paragraph = postprocess_paragraph(paragraph)
    assert processed_paragraph == paragraph
