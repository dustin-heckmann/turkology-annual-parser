# -*- coding: utf-8 -*-

import logging
import re
from dataclasses import replace
from typing import List, Union, Optional, Iterator

import regex

from citation.citation import Citation, CitationType
from citation.field_parsing import parse_name
from citation.intermediate_citation import IntermediateCitation

number_rest_pattern = re.compile(r'(\d+)\.\s*(.+)', re.DOTALL)
fully_parsed_pattern = re.compile(r'({{{\s*[\w_]+\s*}}}[., ]*)+')


def parse_citation(raw_citation: IntermediateCitation) -> IntermediateCitation:
    logging.debug('Parsing citation: {}'.format(raw_citation))
    citation = replace(raw_citation)

    # TODO: Improve
    if not citation.remaining_text:
        citation.number, citation.remaining_text = number_rest_pattern.match(raw_citation.raw_text).groups()

    for parse_function in (
            parse_review,
            parse_comment,
            parse_location_and_date,
            parse_materials,
            parse_location_year_pages,
            parse_series,
            parse_published_in,
            parse_in_missing,
            parse_authors,
            parse_editors_translators,
            parse_title,
    ):
        citation = parse_function(citation)
        fully_parsed = fully_parsed_pattern.fullmatch(citation.remaining_text) is not None
    return replace(citation, fully_parsed=fully_parsed)


def parse_review(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    review_pattern = re.compile(r' +(Rez\.|Abstract +in:) (.*)$')
    review_match = review_pattern.search(text)
    if review_match:
        review_type = review_match.group(1)
        if review_type == 'Rez.':
            citation.reviews = review_match.group(2)
            citation.remaining_text = citation.remaining_text[:review_match.span()[0]] + ' {{{ reviews }}}'
        elif re.sub(' {2,}', ' ', review_type).lower() == 'abstract in:':
            citation.abstract_in = review_match.group(2)
            citation.remaining_text = citation.remaining_text[:review_match.span()[0]] + ' {{{ abstract_in }}}'
    return citation


def parse_comment(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    comment_pattern = re.compile(r'\[([^\]]+)\]\.?( {{{ reviews }}})?$')
    ta_references_pattern = re.compile(r's\. (?:TA \d+(?:-\d+)?\.\d+)(?:, \d(?:-\d+)?\.\d+)*')
    comment_match = comment_pattern.search(text)
    if comment_match:
        comment = comment_match.group(1).strip().rstrip('.')
        ta_references_match = ta_references_pattern.fullmatch(comment)
        if ta_references_match:
            comment_field_name = 'ta_references'
            citation.ta_references = comment
        else:
            comment_field_name = 'comment'
            citation.comment = comment
        text = text[:comment_match.span()[0]] + ' {{{ %s }}}' % comment_field_name
        if comment_match.group(2):
            text += comment_match.group(2)
    return replace(citation, remaining_text=text)


def parse_location_and_date(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    loc_date_pattern = re.compile(
        r'^([^,]+), *((?:\d{1,2}\. *(?:(?:[IVX]{1,4})\. *)?(?:\d{4})?[-—])?\d{1,2}\. *[IVX]{1,4}\. *\d{4})'
    )
    volumes_loc_year_pattern = re.compile(
        r'(\d+) *Bde[.,]+ *(\w+), (\d{4}(?:[-—]\d{4}|(?: *, *\d{4})+)?)(?:, *([\d, +]+) *[Ss]\.)?'
    )
    match = loc_date_pattern.search(text)
    if match:
        citation.location = match.group(1)
        citation.date = match.group(2)
        citation.type = CitationType.CONFERENCE
        text = '{{{ location }}} {{{ date }}} ' + text[match.span()[1]:]
    match = volumes_loc_year_pattern.search(text)
    if match:
        citation.number_of_volumes = match.group(1)
        citation.location = match.group(2)
        citation.date_published = match.group(3)
        if match.group(4):
            citation.number_of_pages = match.group(4).strip()
        text = text[:match.span()[0]] \
               + ' {{{ number_of_volumes }}} {{{ location }}} {{{ date_published }}} ' \
               + text[match.span()[1]:]
    return replace(citation, remaining_text=text)


def parse_materials(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    material_pattern = re.compile(
        r', (\[?\d+\]? *(?:(?:Karte|Tafel|Tabelle|Falt(?:tafel|karte|tabelle))n?|Porträts?|Abb\.|Tab\.|(?:Falt|Schlacht)pl(?:an|äne)))(\.)?'
    )
    material_spans = []
    for material_match in re.finditer(material_pattern, text):
        citation.material.append(material_match.group(1))
        material_spans.append((material_match.span(1)[0], material_match.span()[1]))
    if material_spans:
        remaining_text_parts = []
        previous_end = 0
        for start, end in material_spans:
            remaining_text_parts.append(text[previous_end:start])
            remaining_text_parts.append('{{{ material }}}')
            previous_end = end
        remaining_text_parts.append(text[previous_end:])
        text = ''.join(remaining_text_parts)
    return replace(citation, remaining_text=text)


def parse_location_year_pages(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    loc_year_pages_pattern = re.compile(
        r'([.,]) +\[?([^,.]+), *\[?(\d{4})\]?, *(?:([\d +DCLIVX]+) *[Ss]\.|[Ss]\. (\d+)\s*[-—]\s*(\d+))'
    )
    loc_year_pages_match = loc_year_pages_pattern.search(text)
    if loc_year_pages_match:
        citation.location = loc_year_pages_match.group(2).strip()
        citation.date_published = loc_year_pages_match.group(3)
        if loc_year_pages_match.group(4):
            citation.number_of_pages = loc_year_pages_match.group(4).strip()
        else:
            citation.page_start = loc_year_pages_match.group(5)
            citation.page_end = loc_year_pages_match.group(6)
        text = text[:loc_year_pages_match.span()[0]] \
               + loc_year_pages_match.group(1) \
               + ' {{{ location }}} {{{ date_published }}} {{{ number_of_pages }}}' \
               + text[loc_year_pages_match.span()[1]:]
    return replace(citation, remaining_text=text)


def parse_series(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    series_pattern = re.compile(
        r'{{{ (?:number_of_pages|material|date_published) }}}([ .,]*\(([^)]+)\))\. *?(?:$|{{{ comment)'
    )
    series_match = series_pattern.search(text)
    if series_match:
        citation.series = series_match.group(2).strip()
        text = text[:series_match.span(1)[0]] + '{{{ series }}}' + text[series_match.span(1)[1]:]
    return replace(citation, remaining_text=text)


def parse_published_in(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    in_pattern = re.compile(r' +In ?: +([^.]+ *[\d.\-— ();,*S/=und]+)(?:[.,]|({{{))')
    in_match = in_pattern.search(text)
    if in_match:
        citation.published_in = in_match.group(1)
        citation.type = CitationType.ARTICLE
        text = text[:in_match.span()[0]] + ' {{{ in }}}'
        if in_match.group(2):
            text += text[in_match.span(2)[1]:]
        else:
            text += text[in_match.span()[1]:]
    return replace(citation, remaining_text=text)


def parse_in_missing(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    in_missing_pattern = re.compile(r' +([A-Z]+ +(?:\d+(?:-\d+)?)\.(?:\d+(?:-\d+)?\.){2,})(?:[., ]|({{{))')
    in_missing_match = in_missing_pattern.search(text)
    if in_missing_match:
        citation.published_in = in_missing_match.group(1)
        citation.type = CitationType.ARTICLE
        text = text[:in_missing_match.span()[0]] + ' {{{ in }}}'
        if in_missing_match.group(2):
            text += text[in_missing_match.span(2)[1]:]
        else:
            text += text[in_missing_match.span()[1]:]
    return replace(citation, remaining_text=text)


def parse_title(citation: Union[Citation, IntermediateCitation]) -> Union[Citation, IntermediateCitation]:
    citation = replace(citation)
    text = citation.remaining_text
    title_patterns = [
        re.compile(r'{{{ authors }}}\s*(.+?)\s*{{{ (?:in|editors|translators|number_of_volumes|location) }}}'),
        re.compile(r'{{{ authors }}}\s*([^.(]+?)[.,]?\s*{{{'),
        re.compile(
            r'^((?:[^.,(](?!{{{))+?)[.,]?\s*{{{ (?:in|editors|translators|number_of_volumes|comment|location) '
        ),
    ]
    for title_pattern in title_patterns:
        title_match = title_pattern.search(text)
        if title_match:
            citation.title = title_match.group(1).strip().rstrip('.,')
            text = text[:title_match.span(1)[0]] + '{{{ title }}}' + text[title_match.span(1)[1]:]
            break
    return replace(citation, remaining_text=text)


given_names_pattern = r'(?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)(?: (?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)){,3}(?! +\w\.)'
last_name_pattern = r'\*?(?:\w+ ){,2}[\w\'-]+'
last_name_given_names_pattern = '(?:{}, +{})'.format(last_name_pattern, given_names_pattern)
given_names_last_name_pattern = '(?:{} +{})'.format(given_names_pattern, last_name_pattern)
multiple_authors_pattern = re.compile(
    '^{last_given}(?: *([—-]) *(?:{last_given}|{given_last}))+   +'.format(
        last_given=last_name_given_names_pattern,
        given_last=given_names_last_name_pattern
    ),
    re.UNICODE)


def parse_authors(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    author_pattern = re.compile('^({last_given})   +'.format(last_given=last_name_given_names_pattern), re.UNICODE)
    author_pattern_volume_1 = re.compile(r'^(%s\.):?(?<!geb\.) (?!{{{)+' % last_name_given_names_pattern, re.UNICODE)
    multiple_authors_match = multiple_authors_pattern.search(text)
    if multiple_authors_match:
        multiple_authors_match = multiple_authors_pattern.search(text)
        citation.authors = multiple_authors_match.group()
        text = '{{{ authors }}} ' + text[multiple_authors_match.span()[1]:].strip()
    if citation.volume == '1':
        author_match = author_pattern_volume_1.search(text)
    else:
        author_match = author_pattern.search(text)
    if author_match:
        citation.authors = author_match.group(1).strip()
        text = '{{{ authors }}} ' + text[author_match.span()[1]:].strip()
    return replace(citation, remaining_text=text)


def parse_editors_translators(citation: IntermediateCitation) -> IntermediateCitation:
    citation = replace(citation)
    text = citation.remaining_text
    role_person_pattern = re.compile(
        r'\. *({given_last}) (ed|trs)\.'.format(given_last=given_names_last_name_pattern)
    )
    role_persons_pattern = re.compile(
        r'\. ({given_last}(?: *([—,]| und ) *{given_last})+) (ed|trs)\.'.format(
            given_last=given_names_last_name_pattern)
    )

    multiple_role_persons_match = role_persons_pattern.search(text)
    if multiple_role_persons_match:
        role_name = {'ed': 'editors', 'trs': 'translators'}[multiple_role_persons_match.group(3)]
        setattr(
            citation,
            role_name,
            multiple_role_persons_match.group(1).strip()
        )
        text = text[:multiple_role_persons_match.span(1)[0]] \
               + (' {{{ %s }}} ' % role_name) \
               + text[multiple_role_persons_match.span()[1]:]
    role_person_match = role_person_pattern.search(text)
    if role_person_match:
        role_name = {'ed': 'editors', 'trs': 'translators'}[role_person_match.group(2)]
        setattr(citation, role_name, role_person_match.group(1))
        text = text[:role_person_match.span(1)[0]] \
               + (' {{{ %s }}} ' % role_name) \
               + text[role_person_match.span()[1]:]
    if citation.editors:
        citation.type = CitationType.COLLECTION
    return replace(citation, remaining_text=text)


def find_multiple_authors(citation: Citation, known_authors_pattern) -> Optional[Citation]:
    multiple_authors_pattern = regex.compile(
        r'^({}){{e<=1}}(?: +(?:—|-) +({}){{e<=1}})+\.?\s+(\p{{Lu}}[^ .]+ .+)'
            .format(known_authors_pattern, known_authors_pattern),
            regex.UNICODE | regex.IGNORECASE | regex.DOTALL)
    authors_match = multiple_authors_pattern.findall(citation.remaining_text)
    if authors_match:
        authors_match = authors_match[0]
        author_names = [name for name in authors_match[:-1] if name]
        remaining_text = '{{{ authors }}} ' + authors_match[-1]
        citation.remaining_text = remaining_text
        citation.authors = [parse_name(name) for name in author_names]
        return citation


def find_known_authors(citations: List[Citation], known_authors: Iterator[str]) -> Iterator[Citation]:
    known_authors_pattern = '|'.join([re.escape(author) for author in known_authors])
    for citation in citations:
        if not citation.authors:
            citation = (
                    find_multiple_authors(citation, known_authors_pattern)
                    or find_authors(citation, known_authors_pattern)
                    or citation
            )
        yield reparse_citation(citation)


def reparse_citation(citation: Citation) -> Citation:
    if not citation.title:
        citation = parse_title(citation)
    return citation


def find_authors(citation: Citation, known_authors_pattern) -> Optional[Citation]:
    citation = replace(citation)
    authors_pattern = regex.compile(
        r'^({}){{e<=1}}\.?\s+(\p{{Lu}}[^ .]+ )'.format(known_authors_pattern),
        regex.UNICODE | regex.IGNORECASE
    )
    author_match = authors_pattern.search(citation.remaining_text)

    if author_match:
        author_name = author_match.group(1)
        remaining_text = '{{{ authors }}} ' + citation.remaining_text[author_match.span(2)[0]:]
        citation.remaining_text = remaining_text
        if fully_parsed_pattern.fullmatch(remaining_text):
            citation.fully_parsed = True
        citation.authors = [parse_name(author_name)]
        return citation
