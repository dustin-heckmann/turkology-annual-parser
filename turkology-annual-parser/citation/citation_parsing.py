# -*- coding: utf-8 -*-

import logging
import re
from dataclasses import replace
from typing import List

import regex

from citation.citation import Citation, CitationType
from citation.field_parsing import parse_authors, parse_name
from citation.intermediate_citation import IntermediateCitation


class CitationParser(object):
    given_names_pattern = '(?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)(?: (?:\w{1,2}\.(?:-\w{1,2}\.)?|[\w-]+)){,3}(?! +\w\.)'
    last_name_pattern = '\*?(?:\w+ ){,2}[\w\'-]+'

    last_name_given_names_pattern = '(?:{}, +{})'.format(last_name_pattern, given_names_pattern)
    given_names_last_name_pattern = '(?:{} +{})'.format(given_names_pattern, last_name_pattern)

    number_rest_pattern = re.compile('(\d+)\.\s*(.+)', re.DOTALL)
    review_pattern = re.compile(' +(Rez\.|Abstract +in:) (.*)$')
    comment_pattern = re.compile('\[([^\]]+)\]\.?( {{{ reviews }}})?$')
    material_pattern = re.compile(
        ', (\[?\d+\]? *(?:(?:Karte|Tafel|Tabelle|Falt(?:tafel|karte|tabelle))n?|Porträts?|Abb\.|Tab\.|(?:Falt|Schlacht)pl(?:an|äne)))(\.)?')
    loc_year_pages_pattern = re.compile(
        r'([.,]) +\[?([^,.]+), *\[?(\d{4})\]?, *(?:([\d +DCLIVX]+) *[Ss]\.|[Ss]\. (\d+)\s*[-—]\s*(\d+))')
    loc_date_pattern = re.compile(
        '^([^,]+), *((?:\d{1,2}\. *(?:(?:[IVX]{1,4})\. *)?(?:\d{4})?[-—])?\d{1,2}\. *[IVX]{1,4}\. *\d{4})'
    )
    volumes_loc_year_pattern = re.compile(
        '(\d+) *Bde[.,]+ *(\w+), (\d{4}(?:[-—]\d{4}|(?: *, *\d{4})+)?)(?:, *([\d, +]+) *[Ss]\.)?')
    in_pattern = re.compile(' +In ?: +([^.]+ *[\d.\-— ();,*S/=und]+)(?:[.,]|({{{))')
    in_missing_pattern = re.compile(' +([A-Z]+ +(?:\d+(?:-\d+)?)\.(?:\d+(?:-\d+)?\.){2,})(?:[., ]|({{{))')

    author_pattern = re.compile('^({last_given})   +'.format(last_given=last_name_given_names_pattern), re.UNICODE)
    author_pattern_volume_1 = re.compile('^(%s\.):?(?<!geb\.) (?!{{{)+' % last_name_given_names_pattern, re.UNICODE)
    multiple_authors_pattern = re.compile(
        '^{last_given}(?: *([—-]) *(?:{last_given}|{given_last}))+   +'.format(last_given=last_name_given_names_pattern,
                                                                               given_last=given_names_last_name_pattern),
        re.UNICODE)
    role_person_pattern = re.compile('\. *({given_last}) (ed|trs)\.'.format(given_last=given_names_last_name_pattern))
    role_persons_pattern = re.compile(
        '\. ({given_last}(?: *([—,]| und ) *{given_last})+) (ed|trs)\.'.format(
            given_last=given_names_last_name_pattern))
    title_patterns = [
        re.compile('{{{ authors }}}\s*(.+)\s*{{{ (?:in|editors|translators|number_of_volumes) }}}'),
        re.compile('{{{ authors }}}\s*([^.(]+?)[.,]?\s*{{{'),
        re.compile('^((?:[^.,(](?!{{{))+?)[.,]?\s*{{{ (?:in|editors|translators|number_of_volumes|comment|location) '),
    ]
    series_pattern = re.compile(
        '{{{ (?:number_of_pages|material|date_published) }}}([ .,]*\(([^)]+)\))\. *?(?:$|{{{ comment)')

    ta_references_pattern = re.compile('s\. (?:TA \d(?:-\d+)?\.\d+)(?:, \d(?:-\d+)?\.\d+)*')

    fully_parsed_pattern = re.compile('({{{\s*[\w_]+\s*}}}[., ]*)+')

    @classmethod
    def parse_citation(cls, raw_citation: IntermediateCitation) -> IntermediateCitation:
        logging.debug('Parsing citation: {}'.format(raw_citation))
        citation = replace(raw_citation)
        if citation.remaining_text:
            text = citation.remaining_text
        else:
            citation_number, text = cls.number_rest_pattern.match(raw_citation.raw_text).groups()
            citation.number = citation_number

        review_match = cls.review_pattern.search(text)
        if review_match:
            review_type = review_match.group(1)
            if review_type == 'Rez.':
                field_name = 'reviews'
                # citation._raw[field_name] = re.split('\s*—\s*', review_match.group(2))
                citation.reviews = review_match.group(2)
            elif re.sub(' {2,}', ' ', review_type).lower() == 'abstract in:':
                field_name = 'abstract_in'
                citation.abstract_in = review_match.group(2)
            text = text[:review_match.span()[0]] + (' {{{ %s }}}' % field_name)

        comment_match = cls.comment_pattern.search(text)
        if comment_match:
            comment = comment_match.group(1).strip().rstrip('.')
            ta_references_match = cls.ta_references_pattern.fullmatch(comment)
            if ta_references_match:
                comment_field_name = 'ta_references'
                citation.ta_references = comment
            else:
                comment_field_name = 'comment'
                citation.comment = comment
            text = text[:comment_match.span()[0]] + ' {{{ %s }}}' % comment_field_name
            if comment_match.group(2):
                text += comment_match.group(2)

        match = cls.loc_date_pattern.search(text)
        if match:
            citation.location = match.group(1)
            citation.date = match.group(2)
            citation.type = CitationType.CONFERENCE
            text = '{{{ location }}} {{{ date }}} ' + text[match.span()[1]:]

        match = cls.volumes_loc_year_pattern.search(text)
        if match:
            citation.number_of_volumes = match.group(1)
            citation.location = match.group(2)
            citation.date_published = match.group(3)
            if match.group(4):
                citation.number_of_pages = match.group(4).strip()
            text = text[:match.span()[0]] \
                   + ' {{{ number_of_volumes }}} {{{ location }}} {{{ date_published }}} ' \
                   + text[match.span()[1]:]

        material_spans = []
        for material_match in re.finditer(cls.material_pattern, text):
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

        loc_year_pages_match = cls.loc_year_pages_pattern.search(text)
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

        series_match = cls.series_pattern.search(text)
        if series_match:
            citation.series = series_match.group(2).strip()
            text = text[:series_match.span(1)[0]] + '{{{ series }}}' + text[series_match.span(1)[1]:]

        in_match = cls.in_pattern.search(text)
        if in_match:
            citation.published_in = in_match.group(1)
            citation.type = CitationType.ARTICLE
            text = text[:in_match.span()[0]] + ' {{{ in }}}'
            if in_match.group(2):
                text += text[in_match.span(2)[1]:]
            else:
                text += text[in_match.span()[1]:]

        in_missing_match = cls.in_missing_pattern.search(text)
        if in_missing_match:
            citation.published_in = in_missing_match.group(1)
            citation.type = CitationType.ARTICLE
            text = text[:in_missing_match.span()[0]] + ' {{{ in }}}'
            if in_missing_match.group(2):
                text += text[in_missing_match.span(2)[1]:]
            else:
                text += text[in_missing_match.span()[1]:]

        multiple_authors_match = cls.multiple_authors_pattern.search(text)
        if multiple_authors_match:
            citation.authors = multiple_authors_match.group()  # .split(multiple_authors_match.group(1))]
            text = '{{{ authors }}} ' + text[multiple_authors_match.span()[1]:].strip()

        if citation.volume == '1':
            author_match = cls.author_pattern_volume_1.search(text)
        else:
            author_match = cls.author_pattern.search(text)
        if author_match:
            citation.authors = author_match.group(1).strip()
            text = '{{{ authors }}} ' + text[author_match.span()[1]:].strip()

        multiple_role_persons_match = cls.role_persons_pattern.search(text)
        if multiple_role_persons_match:
            role_name = {'ed': 'editors', 'trs': 'translators'}[multiple_role_persons_match.group(3)]
            setattr(
                citation,
                role_name,
                multiple_role_persons_match.group(1).strip()  # .split(multiple_role_persons_match.group(2))
            )
            text = text[:multiple_role_persons_match.span(1)[0]] \
                   + (' {{{ %s }}} ' % role_name) \
                   + text[multiple_role_persons_match.span()[1]:]
        role_person_match = cls.role_person_pattern.search(text)
        if role_person_match:
            role_name = {'ed': 'editors', 'trs': 'translators'}[role_person_match.group(2)]
            setattr(citation, role_name, role_person_match.group(1))
            text = text[:role_person_match.span(1)[0]] \
                   + (' {{{ %s }}} ' % role_name) \
                   + text[role_person_match.span()[1]:]

        if citation.editors:
            citation.type = CitationType.COLLECTION

        for title_pattern in cls.title_patterns:
            title_match = title_pattern.search(text)
            if title_match:
                citation.title = title_match.group(1).strip().rstrip('.,')
                text = text[:title_match.span(1)[0]] + '{{{ title }}}' + text[title_match.span(1)[1]:]
                break

        citation.remaining_text = text
        citation.fully_parsed = cls.fully_parsed_pattern.fullmatch(text) is not None
        return citation

    def find_multiple_authors(self, citation, known_authors_pattern):
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

    def find_authors(self, citation, known_authors_pattern):
        citation = replace(citation)
        authors_pattern = regex.compile(r'^({}){{e<=1}}\.?\s+(\p{{Lu}}[^ .]+ )'.format(known_authors_pattern),
                                        regex.UNICODE | regex.IGNORECASE)
        author_match = authors_pattern.search(citation.remaining_text)

        if author_match:
            author_name = author_match.group(1)
            remaining_text = '{{{ authors }}} ' + citation.remaining_text[author_match.span(2)[0]:]
            citation.remaining_text = remaining_text
            if self.fully_parsed_pattern.fullmatch(remaining_text):
                citation.fully_parsed = True
            citation.authors = [parse_name(author_name)]
            return citation

    def find_known_authors(self, citations: List[Citation], known_authors):
        known_authors_pattern = '|'.join([re.escape(author) for author in known_authors])
        for citation in citations:
            if not citation.authors:
                citation = (
                        self.find_multiple_authors(citation, known_authors_pattern)
                        or self.find_authors(citation, known_authors_pattern)
                        or citation
                )
                if citation.authors:
                    pass#print(citation.volume, citation.number)
            yield citation
