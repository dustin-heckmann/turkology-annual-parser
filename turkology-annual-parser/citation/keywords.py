import re

raw_keyword_pattern = re.compile(r'(?P<code>[A-Za-z]+)(?:\..+)?')


def normalize_keywords_for_citation(citation, keyword_mapping):
    normalized_keywords = []
    raw_keywords = citation.get('keywords', [])
    already_seen_codes = set(raw_keywords)
    while raw_keywords:
        raw_keyword = raw_keywords.pop()
        raw_keyword = raw_keyword \
            .replace('Α', 'A') \
            .replace('Β', 'B') \
            .replace('Ή', 'H') \
            .replace('DΠ', 'DII') \
            .replace('dľf.', 'DIF.') \
            .replace(r'DJx\C.', 'DJAC.') \
            .replace('dha A.', 'DH.') \
            .replace('Bí.', 'BI')
        #  Wrong detection of characters (e.g. alpha instead of a)
        raw_keyword_match = raw_keyword_pattern.fullmatch(raw_keyword)
        if not raw_keyword_match:
            split_code_match = re.search('^([A-Z ]+)\.', raw_keyword)  # Extraneous whitespace
            if split_code_match:
                fixed_raw_keyword = split_code_match.group(1).replace(' ', '') + raw_keyword[raw_keyword.index('.'):]
                raw_keyword_match = raw_keyword_pattern.fullmatch(fixed_raw_keyword)
        if not raw_keyword_match:  # Trailing period missing
            raw_keyword_match = re.fullmatch(r'(?P<code>[A-Z]+) .+', raw_keyword)
        if raw_keyword_match:
            code = raw_keyword_match.group('code')
            if code.upper() in keyword_mapping:
                code = code.upper()
                keyword = {
                    'code': code,
                    'nameDE': keyword_mapping[code][0],
                    'nameEN': keyword_mapping[code][1],
                    'raw': None if raw_keyword.endswith('___') else raw_keyword,
                }
            else:
                keyword = {
                    'raw': raw_keyword,
                    'code': code,
                }
            if len(code) > 1:
                for i in range(1, len(code)):
                    sub_code = code[:i]
                    if sub_code not in already_seen_codes:
                        raw_keywords.append(f'{sub_code}. ___')
                        already_seen_codes.add(sub_code)
            normalized_keywords.append(keyword)
        else:
            print(f'WARNING: No keyword code found in >{raw_keyword}<')
            normalized_keywords.append({
                'raw': raw_keyword,
            })
    if normalized_keywords:
        citation['keywords'] = normalized_keywords
    return citation
