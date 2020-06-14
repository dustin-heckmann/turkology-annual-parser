# -*- coding: utf-8 -*-

import logging
import re
from dataclasses import replace
from typing import Union, Iterable

from domain.citation import Citation, CitationType
from domain.intermediate_citation import IntermediateCitation

number_rest_pattern = re.compile(r'(\d+)\.\s*(.+)', re.DOTALL)


def parse_citations(citations: Iterable[IntermediateCitation]) -> Iterable[IntermediateCitation]:
    return (parse_citation(citation) for citation in citations)


def parse_citation(citation: IntermediateCitation) -> IntermediateCitation:
    logging.debug('Parsing citation: {}'.format(citation))

    # TODO: Improve
    if not citation.remaining_text:  # Citation has not already been parsed
        number_text_match = number_rest_pattern.match(citation.raw_text)
        if not number_text_match:
            raise ValueError(
                f'Citation does not match basic citation pattern of number & text:\n{str(citation)}'
            )
        number, remaining_text = number_text_match.groups()
        citation = replace(citation, number=number, remaining_text=remaining_text)

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
    return citation


def parse_review(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    review_pattern = re.compile(r' +(Rez\.|Abstract +in:) (.*)$')
    review_match = review_pattern.search(text)
    if review_match:
        review_type = review_match.group(1)
        if review_type == 'Rez.':
            citation = replace(
                citation,
                reviews=review_match.group(2),
                remaining_text=citation.remaining_text[:review_match.span()[0]] + ' {{{ reviews }}}'
            )
        elif re.sub(' {2,}', ' ', review_type).lower() == 'abstract in:':
            citation = replace(
                citation,
                abstract_in=review_match.group(2),
                remaining_text=citation.remaining_text[
                               :review_match.span()[0]] + ' {{{ abstract_in }}}'
            )
    return citation


def parse_comment(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    comment_pattern = re.compile(r'\[([^\]]+)\]\.?( {{{ reviews }}})?$')
    ta_references_pattern = re.compile(r's\. (?:TA \d+(?:-\d+)?\.\d+)(?:, \d(?:-\d+)?\.\d+)*')
    comment_match = comment_pattern.search(text)
    if not comment_match:
        return citation

    comment = comment_match.group(1).strip().rstrip('.')
    ta_references_match = ta_references_pattern.fullmatch(comment)
    if ta_references_match:
        comment_field_name = 'ta_references'
        citation = replace(citation, ta_references=comment)
    else:
        comment_field_name = 'comment'
        citation = replace(citation, comment=comment)
    text = text[:comment_match.span()[0]] + ' {{{ %s }}}' % comment_field_name
    if comment_match.group(2):
        text += comment_match.group(2)
    return replace(citation, remaining_text=text)


def parse_location_and_date(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    loc_date_pattern = re.compile(
        r'^([^,]+), *((?:\d{1,2}\. *(?:(?:[IVX]{1,4})\. *)?'
        r'(?:\d{4})?[-—])?\d{1,2}\. *[IVX]{1,4}\. *\d{4})'
    )
    volumes_loc_year_pattern = re.compile(
        r'(\d+) *Bde[.,]+ *(\w+), (\d{4}(?:[-—]\d{4}|(?: *, *\d{4})+)?)(?:, *([\d, +]+) *[Ss]\.)?'
    )
    match = loc_date_pattern.search(text)
    if match:
        citation = replace(
            citation,
            location=match.group(1),
            date=match.group(2),
            type=CitationType.CONFERENCE,
        )
        text = '{{{ location }}} {{{ date }}} ' + text[match.span()[1]:]

    match = volumes_loc_year_pattern.search(text)
    if match:
        citation = replace(
            citation,
            number_of_volumes=match.group(1),
            location=match.group(2),
            date_published=match.group(3),
        )

        if match.group(4):
            citation = replace(citation, number_of_pages=match.group(4).strip())
        text = ''.join((
            text[:match.span()[0]],
            ' {{{ number_of_volumes }}} {{{ location }}} {{{ date_published }}} ',
            text[match.span()[1]:],
        ))
    return replace(citation, remaining_text=text)


def parse_materials(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    material_pattern = re.compile(
        r', (\[?\d+\]? *(?:(?:Karte|Tafel|Tabelle|Falt(?:tafel|karte|tabelle))n?'
        r'|Porträts?|Abb\.|Tab\.|(?:Falt|Schlacht)pl(?:an|äne)))(\.)?'
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
    text = citation.remaining_text
    loc_year_pages_pattern = re.compile(
        r'([.,?]) +\[?'
        r'([^,.?]+)'  # location
        r', *\[?'  # comma, 0+ spaces, maybe opening square bracket
        r'(\d{4})'  # date_published (year)
        r'\]?[,.] *'
        r'(?:'
        r'([\d +DCLIVX]+)'  # number of pages (arabic / roman)
        r' *[Ss]\.|[Ss]\. '  # S. (abbreviation for "Seiten")
        r'(\d+)'  # pageStart
        r'\s*[-—]\s*'
        r'(\d+))'  # pageEnd
    )
    loc_year_pages_match = loc_year_pages_pattern.search(text)
    if loc_year_pages_match:
        citation = replace(
            citation,
            location=loc_year_pages_match.group(2).strip(),
            date_published=loc_year_pages_match.group(3),
        )

        if loc_year_pages_match.group(4):
            # numberOfPages
            citation = replace(
                citation,
                number_of_pages=loc_year_pages_match.group(4).strip()
            )
        else:
            citation = replace(
                citation,
                page_start=loc_year_pages_match.group(5),
                page_end=loc_year_pages_match.group(6),
            )

        text = ''.join((
            text[:loc_year_pages_match.span()[0]],
            loc_year_pages_match.group(1),
            ' {{{ location }}} {{{ date_published }}} {{{ number_of_pages }}}',
            text[loc_year_pages_match.span()[1]:],
        ))
    return replace(citation, remaining_text=text)


def parse_series(citation: IntermediateCitation) -> IntermediateCitation:
    series_pattern = re.compile(
        r'{{{ (?:number_of_pages|material|date_published) }}}'
        r'([ .,]*\(([^)]+)\))\. *?(?:$|{{{ comment)'
    )
    series_match = series_pattern.search(citation.remaining_text)
    if series_match:
        remaining_text = citation.remaining_text[:series_match.span(1)[0]] \
                         + '{{{ series }}}' \
                         + citation.remaining_text[series_match.span(1)[1]:]
        return replace(
            citation,
            series=series_match.group(2).strip(),
            remaining_text=remaining_text,
        )
    return citation


def parse_published_in(citation: IntermediateCitation) -> IntermediateCitation:
    in_pattern = re.compile(r' +In ?: +([^.]+ *[\d.\-— ();,*S/=und]+)(?:[.,]|({{{))')
    in_match = in_pattern.search(citation.remaining_text)
    if in_match:
        text = citation.remaining_text[:in_match.span()[0]] + ' {{{ in }}}'
        if in_match.group(2):
            text += text[in_match.span(2)[1]:]
        else:
            text += text[in_match.span()[1]:]
        return replace(
            citation,
            published_in=in_match.group(1),
            type=CitationType.ARTICLE,
            remaining_text=text,
        )
    return citation


def parse_in_missing(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    in_missing_pattern = re.compile(
        r' +([A-Z]+ +(?:\d+(?:-\d+)?)\.(?:\d+(?:-\d+)?\.){2,})(?:[., ]|({{{))')
    in_missing_match = in_missing_pattern.search(text)
    if in_missing_match:
        text = text[:in_missing_match.span()[0]] + ' {{{ in }}}'
        if in_missing_match.group(2):
            text += text[in_missing_match.span(2)[1]:]
        else:
            text += text[in_missing_match.span()[1]:]
        return replace(
            citation,
            published_in=in_missing_match.group(1),
            type=CitationType.ARTICLE,
            remaining_text=text,
        )
    return citation


def parse_title(
        citation: Union[Citation, IntermediateCitation]
) -> Union[Citation, IntermediateCitation]:
    title_patterns = [
        re.compile(
            r'{{{ authors }}}\s*(.+?)\s*'
            r'{{{ (?:in|editors|translators|number_of_volumes|location) }}}'
        ),
        re.compile(r'{{{ authors }}}\s*([^.(]+?)[.,]?\s*{{{'),
        re.compile(
            r'^((?:[^.,(](?!{{{))+?)[.,]?\s*'
            r'{{{ (?:in|editors|translators|number_of_volumes|comment|location) '
        ),
    ]
    for title_pattern in title_patterns:
        title_match = title_pattern.search(citation.remaining_text)
        if title_match:
            text = citation.remaining_text[:title_match.span(1)[0]] \
                   + '{{{ title }}}' \
                   + citation.remaining_text[title_match.span(1)[1]:]
            return replace(
                citation,
                title=title_match.group(1).strip().rstrip('.,'),
                remaining_text=text,
            )
    return citation


given_names_pattern = r'(?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)' \
                      r'(?: (?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)){,3}(?! +\w\.)'
last_name_pattern = r'\*?(?:\w+ ){,2}[\w\'-]+'
last_name_given_names_pattern = '(?:{}, +{})'.format(last_name_pattern, given_names_pattern)
given_names_last_name_pattern = '(?:{} +{})'.format(given_names_pattern, last_name_pattern)
multiple_authors_pattern = re.compile(
    f'^{last_name_given_names_pattern}(?: *([—-]) *(?:{last_name_given_names_pattern}'
    f'|{given_names_last_name_pattern}))+ {{3,}}',
    re.UNICODE
)


def parse_authors(citation: IntermediateCitation) -> IntermediateCitation:
    text = citation.remaining_text
    author_pattern = re.compile(f'^({last_name_given_names_pattern}) {{2}} +', re.UNICODE)
    author_pattern_volume_1 = re.compile(
        r'^(%s\.):?(?<!geb\.) (?!{{{)+' % last_name_given_names_pattern, re.UNICODE)
    multiple_authors_match = multiple_authors_pattern.search(text)
    if multiple_authors_match:
        # multiple_authors_match = multiple_authors_pattern.search(text) # Probably pointless
        return replace(
            citation,
            authors=multiple_authors_match.group(),
            remaining_text=' '.join((
                '{{{ authors }}}',
                text[multiple_authors_match.span()[1]:].strip()
            ))
        )
    if citation.volume == '1':
        author_match = author_pattern_volume_1.search(text)
    else:
        author_match = author_pattern.search(text)
    if author_match:
        return replace(
            citation,
            authors=author_match.group(1).strip(),
            remaining_text='{{{ authors }}} ' + text[author_match.span()[1]:].strip(),
        )
    return citation


def parse_editors_translators(citation: IntermediateCitation) -> IntermediateCitation:
    role_person_pattern = re.compile(
        r'\. *({given_last}) (ed|trs)\.'.format(given_last=given_names_last_name_pattern)
    )
    role_persons_pattern = re.compile(
        r'\. ({given_last}(?: *([—,]| und ) *{given_last})+) (ed|trs)\.'.format(
            given_last=given_names_last_name_pattern)
    )

    multiple_role_persons_match = role_persons_pattern.search(citation.remaining_text)
    if multiple_role_persons_match:
        role_name = {'ed': 'editors', 'trs': 'translators'}[multiple_role_persons_match.group(3)]
        return replace(
            citation,
            remaining_text=''.join((
                citation.remaining_text[:multiple_role_persons_match.span(1)[0]],
                (' {{{ %s }}} ' % role_name),
                citation.remaining_text[multiple_role_persons_match.span()[1]:],
            )),
            type=CitationType.COLLECTION if role_name == 'editors' else None,
            **{role_name: multiple_role_persons_match.group(1).strip()},
        )

    role_person_match = role_person_pattern.search(citation.remaining_text)
    if role_person_match:
        role_name = {'ed': 'editors', 'trs': 'translators'}[role_person_match.group(2)]
        return replace(
            citation,
            remaining_text=''.join((
                citation.remaining_text[:role_person_match.span(1)[0]],
                (' {{{ %s }}} ' % role_name),
                citation.remaining_text[role_person_match.span()[1]:],
            )),
            type=CitationType.COLLECTION if role_name == 'editors' else None,
            **{role_name: role_person_match.group(1)},
        )
    return citation


def reparse_citation(citation: Citation) -> Citation:
    if not citation.title:
        citation = parse_title(citation)
    return citation
