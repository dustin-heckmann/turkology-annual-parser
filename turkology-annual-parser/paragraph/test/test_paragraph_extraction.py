from unittest.mock import patch

from paragraph.paragraph_extraction import extract_volume_from_filename, extract_paragraphs


@patch('paragraph.paragraph_extraction.WMLParser')
def test_extract_paragraphs(WMLParser):
    WMLParser.return_value = iter([{'text': 'some text'}, {'text': 'some more'}])
    paragraphs = list(extract_paragraphs('TA99_01.xml'))
    assert paragraphs == [
        {
            'text': 'some text',
            'volume': '99'
        },
        {
            'text': 'some more',
            'volume': '99'
        }
    ]


def test_extract_volume_from_filename_vol_01():
    file_path = 'data/ocr/TA01_02_Xhosa_WML_formatted_pb_nopic_patterns.xml'
    assert extract_volume_from_filename(file_path) == '1'


def test_extract_volume_from_filename_vol_22_23():
    file_path = 'data/ocr/TA22-23_03_Xhosa_patterns.xml'
    assert extract_volume_from_filename(file_path) == '22-23'


def test_extract_volume_from_filename_vol_26():
    file_path = 'TA26_02_Xhosa_formatted_pb_nopics.xml'
    assert extract_volume_from_filename(file_path) == '26'