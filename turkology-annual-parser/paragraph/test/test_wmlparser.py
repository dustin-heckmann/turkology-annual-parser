import os
from itertools import islice

from paragraph.paragraph import Paragraph
from paragraph.wmlparser import WMLParser

TA01 = 'TA01_02_Xhosa_WML_formatted_pb_nopic_patterns.xml'
TA26 = 'TA26_02_Xhosa_formatted_pb_nopics.xml'


def test_parser_gets_correct_number_of_paragraphs_vol_1():
    parser = WMLParser(get_xml_path(TA01))
    assert len(list(parser)) == 3332


def test_parser_returns_specific_paragraphs_vol_1():
    parser = WMLParser(get_xml_path(TA01))
    paragraphs = list(islice(parser, 1200, 1202))
    assert paragraphs == [
        Paragraph(
            originalIndex=1200,
            text='Rez. Wilhelm Wagner, ÖO 15.4.1973.443-445. — Anton Scherer, SODV '
                 '23.3.1974.219-220. — Helmut Schnitter, MM 13.3.1974. 364-365.'),
        Paragraph(
            originalIndex=1201,
            text='# Zu den Handelsbeziehungen mit Österreich, s. 1060.'
        )
    ]


def test_parser_gets_correct_number_of_paragraphs_vol_26():
    parser = WMLParser(get_xml_path(TA26))
    assert len(list(parser)) == 7138


def test_parser_returns_specific_paragraphs_vol_26():
    parser = WMLParser(get_xml_path(TA26))
    paragraphs = list(islice(parser, 5560, 5562))
    assert paragraphs == [
        Paragraph(
            originalIndex=5560,
            text='3643. Şçerbak, Α. Μ.    Ulangom yazıtı üzerine ilâve düşünceler. In: TDAYB 1994(1996).131-136.'
        ),
        Paragraph(
            originalIndex=5561,
            text='3644. Scharlipp, Wolfgang-Ε.      Inverted syntax in early Turkish texts. In: TA 26.314.235-243. [Betrifft Alt- und Mitteltürkisch.]'
        )
    ]


def get_xml_path(filename): return os.path.join(os.path.dirname(__file__), '../../../data/ocr/', filename)
