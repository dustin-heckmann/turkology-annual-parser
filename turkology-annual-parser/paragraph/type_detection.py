from dataclasses import replace
from typing import Dict, List

import regex as re

from domain.paragraph import Paragraph, ParagraphType

MAX_CITATION_GAP = 500

KNOWN_CITATION_GAPS_BY_VOLUME = {  # Ranges are inclusive
    '6': (
        (1823, 1831),
        (1871, 1883),
        (1894, 1902),
    ),
    '8': (
        (607, 617),
        (629, 638),
    )
}


def detect_paragraph_types(paragraphs: List[Paragraph], keyword_mapping: Dict[str, Dict[str, str]]):
    journal_section_begin_pattern = re.compile('ZEITSCHRIFTEN +UND')
    journal_pattern = re.compile('')
    keyword_pattern_base = '({})'.format(
        '|'.join([
            re.escape('{}. {}'.format(code, translations['de']))
            for code, translations in keyword_mapping.items()
        ])
    )
    keyword_pattern_exact = re.compile(keyword_pattern_base, re.IGNORECASE)
    keyword_pattern_fuzzy = re.compile(keyword_pattern_base + '{e<=2}', re.IGNORECASE)
    citation_pattern = re.compile(r'(\d+)\.\.?\s+.+', re.DOTALL)
    broken_bullet_pattern = re.compile(r'^[φ#0Φ].*')  # , s\.( a\.)? \d+')
    page_number_pattern = re.compile(r'(\d+\s+Turkologischer Anzeiger|Turkologischer Anzeiger\s+\d+){e<=2}')

    citation_section_has_begun = False
    latest_citation_number = 0
    previous_type = None
    index_has_begun = False
    journal_section_has_begun = False

    for paragraph in paragraphs:
        paragraph_type = None
        text = paragraph.text or ''
        is_possible_amendment = previous_type == ParagraphType.CITATION or (
                previous_type and previous_type == ParagraphType.AMENDMENT)
        citation_match = citation_pattern.fullmatch(text)

        if not journal_section_has_begun:
            if journal_section_begin_pattern.search(text):
                paragraph_type = ParagraphType.JOURNAL_SECTION_BEGIN
                journal_section_has_begun = True

        if journal_section_has_begun and not citation_section_has_begun:
            journal_match = journal_pattern.search(text)
            if False and journal_match:
                paragraph_type = ParagraphType.JOURNAL
            elif keyword_pattern_fuzzy.fullmatch(text):
                paragraph_type = ParagraphType.KEYWORD
            elif citation_section_has_begun and text.split('.')[0] in keyword_mapping:
                paragraph_type = ParagraphType.KEYWORD
            if paragraph_type == ParagraphType.KEYWORD:
                citation_section_has_begun = True

        if citation_section_has_begun and not index_has_begun:
            if keyword_pattern_exact.fullmatch(text):
                paragraph_type = ParagraphType.KEYWORD
            elif citation_section_has_begun and citation_match and (
                    0 < (int(citation_match.group(1)) - latest_citation_number) <= MAX_CITATION_GAP
                    or _is_preceded_by_ocr_gap(paragraph.volume, int(citation_match.group(1)))
            ):
                paragraph_type = ParagraphType.CITATION
                latest_citation_number = int(citation_match.group(1))
            elif keyword_pattern_fuzzy.fullmatch(text):
                paragraph_type = ParagraphType.KEYWORD
            elif citation_section_has_begun and text.split('.')[0] in keyword_mapping:
                paragraph_type = ParagraphType.KEYWORD
            elif text.startswith('•') and is_possible_amendment:
                paragraph_type = ParagraphType.AMENDMENT
            elif text.startswith('Rez.') and is_possible_amendment:
                paragraph_type = ParagraphType.AMENDMENT
            elif text.startswith('Bericht') and is_possible_amendment:
                paragraph_type = ParagraphType.AMENDMENT
            elif text == 'Autoren, Herausgeber, Übersetzer, Rezensenten' or text == 'INDEX':
                paragraph_type = ParagraphType.AUTHOR_INDEX_BEGIN
                index_has_begun = True
            elif broken_bullet_pattern.match(text) and is_possible_amendment:
                paragraph_type = ParagraphType.AMENDMENT
            elif citation_section_has_begun and citation_match:
                paragraph_type = ParagraphType.CITATION
                latest_citation_number = int(citation_match.group(1))
        yield replace(paragraph, type=paragraph_type)
        if not page_number_pattern.fullmatch(text):
            previous_type = paragraph_type


def _is_preceded_by_ocr_gap(volume, number):
    for _, range_end in KNOWN_CITATION_GAPS_BY_VOLUME.get(volume, ()):
        if number == range_end + 1:
            return True
    return False
