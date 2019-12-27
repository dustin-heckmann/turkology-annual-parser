import re
from dataclasses import replace
from typing import Dict

from citation.citation import Citation

raw_keyword_pattern = re.compile(r'(?P<code>[A-Za-z]+)(?:\..+)?')


def normalize_keywords_for_citation(citation: Citation, keyword_mapping: Dict[str, Dict[str, str]]):
    keywords = []
    for raw_keyword in citation.keywords:
        raw_keyword = fix_ocr_errors(raw_keyword)
        code = extract_keyword_code(raw_keyword)
        if not code:
            keywords.append({'raw': raw_keyword})
            continue
        keyword = make_keyword(code, keyword_mapping, raw_keyword)
        keywords.append(keyword)
    if keywords:
        citation = replace(citation, keywords=keywords)
    return citation


def make_keyword(code, keyword_mapping, raw_keyword=None):
    if not code:
        return
    if code.upper() in keyword_mapping:
        code = code.upper()
        keyword = {
            'code': code,
            'nameDE': keyword_mapping[code]['de'],
            'nameEN': keyword_mapping[code]['en'],
            'raw': raw_keyword,
            'super': make_keyword(code[:-1], keyword_mapping)
        }

    else:
        keyword = {
            'raw': raw_keyword,
            'code': code,
        }
    return keyword


def extract_keyword_code(raw_keyword):
    raw_keyword = fix_ocr_errors(raw_keyword)
    raw_keyword_match = raw_keyword_pattern.fullmatch(raw_keyword)
    if not raw_keyword_match:
        raw_keyword_match = foo(raw_keyword, raw_keyword_match)
    if not raw_keyword_match:  # Trailing period missing
        raw_keyword_match = re.fullmatch(r'(?P<code>[A-Z]+) .+', raw_keyword)
    if raw_keyword_match:
        return raw_keyword_match.group('code')


def foo(raw_keyword, raw_keyword_match):
    split_code_match = re.search('^([A-Z ]+)\.', raw_keyword)  # Extraneous whitespace
    if split_code_match:
        fixed_raw_keyword = split_code_match.group(1).replace(' ', '') + raw_keyword[raw_keyword.index('.'):]
        raw_keyword_match = raw_keyword_pattern.fullmatch(fixed_raw_keyword)
    return raw_keyword_match


def fix_ocr_errors(raw_keyword):
    """Replace common misclassifications of letters"""
    return raw_keyword \
        .replace('Α', 'A') \
        .replace('Β', 'B') \
        .replace('Ή', 'H') \
        .replace('DΠ', 'DII') \
        .replace('dľf.', 'DIF.') \
        .replace(r'DJx\C.', 'DJAC.') \
        .replace('dha A.', 'DH.') \
        .replace('Bí.', 'BI')
