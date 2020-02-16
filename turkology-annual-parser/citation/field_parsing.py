import re
from datetime import datetime

import nameparser

from citation.citation import Citation, Person
from citation.intermediate_citation import IntermediateCitation


def parse_citation_fields(intermediate: IntermediateCitation) -> Citation:
    reviews, comments = parse_amendments_or_comments([intermediate.comment])
    more_reviews, amendments = parse_amendments_or_comments(intermediate.amendments)
    reviews.extend(more_reviews)
    reviews.extend(parse_reviews(intermediate.reviews))
    return Citation(
        volume=intermediate.volume,
        number=int(intermediate.number),
        type=intermediate.type,
        title=intermediate.title,
        location=intermediate.location,
        series=intermediate.series,
        keywords=[{'raw': keyword} for keyword in intermediate.keywords],
        number_of_volumes=intermediate.number_of_volumes,
        number_of_pages=intermediate.number_of_pages,
        authors=parse_authors(intermediate.authors),
        editors=parse_editors_or_translators(intermediate.editors),
        translators=parse_editors_or_translators(intermediate.translators),
        comments=comments,
        reviews=reviews,
        published_in=parse_reference(intermediate.published_in),
        amendments=amendments,
        date_published=parse_date_published(intermediate.date_published),
        raw_text=intermediate.raw_text,
        material=parse_material(intermediate.material),
        date=parse_date(intermediate.date),
        ta_references=parse_ta_references(intermediate.ta_references),
        remaining_text=intermediate.remaining_text
    )


def parse_amendments_or_comments(texts):
    if not texts:
        return [], []
    unparseable_amendments = []
    reviews = []
    for amendment_string in texts:
        if not amendment_string:
            continue
        bullet_pattern = re.compile(r'^[•φ#0Φ]\s+')  # , s\.( a\.)? \d+')
        amendment_string = re.sub(bullet_pattern, '', amendment_string)
        if amendment_string and amendment_string.startswith('Rez.'):
            amendment_string = re.sub('^Rez\. *', '', amendment_string)
            reviews.extend(re.split(r'\s+—\s+', amendment_string))
        else:
            unparseable_amendments.append(amendment_string)
    return reviews, unparseable_amendments


def parse_reviews(review_str):
    if review_str:
        return re.split(r'\s+—\s+', review_str)
    return []


def parse_authors(authors):
    if authors:
        return list(map(parse_name, re.split(r'(?:—| +- +)', authors)))
    return []


def parse_editors_or_translators(people):
    if people:
        return list(map(parse_name, re.split(r'\s*(?:,| und )\s*', people)))
    return []


def parse_name(name):
    if not isinstance(name, str):
        return name
    parsed_name = nameparser.HumanName(name)
    return Person(
        first=parsed_name.first if parsed_name.first else None,
        middle=parsed_name.middle if parsed_name.middle else None,
        last=parsed_name.last if parsed_name.last else None,
        raw=name
    )


def parse_ta_references(reference_string):
    if not reference_string: return []
    reference_string = re.sub('^s\. TA ', '', reference_string)
    reference_strings = re.split(', ', reference_string)
    references = []
    for reference_string in reference_strings:
        reference_parts = reference_string.split('.')
        references.append({
            'volume': int(reference_parts[0]) if reference_parts[0].isdigit() else reference_parts[0],
            'number': int(reference_parts[1]),
        })
    return references


def parse_amendments(amendment_strings):
    return amendment_strings


year_pattern = '(?:(?P<year>\d{4})|(?P<yearStart>\d{4})[-—/](?P<yearEnd>\d{2}(?:\d{2})?))(?: *\((?P<yearParentheses>\d{4})\))?'
pages_pattern = '(?:S\. ?)?(?P<pageStart>\d+)(?:[-—](?P<pageEnd>\d+))?'
issues_pattern = '(?:(?P<issue>\d{1,3})|(?P<issueStart>\d{1,3})[-—](?P<issueEnd>\d{1,3}))'
volume_pattern = '(?:(?P<volume>\d{1,2})|(?P<volumeStart>\d{1,2})[-—](?P<volumeEnd>\d{1,2}))'
journal_pattern = '(?P<journal>(?:[^\W\d_]|[\- ])+?)'

reference_patterns = [
    ('ta', re.compile('^TA *(?P<volume>\d+)\. *(?P<number>\d+)(?:\. *%s)?$' % pages_pattern)),

    # ('volume.issue.year.pages', re.compile('^ *%s *%s\. *%s\. *%s$' % (year_pattern, issues_pattern, pages_pattern))),  # volume.issue.year.pages
    # ('year.issue.pages', re.compile('^(?P<journal>[\w ]+?) *%s\. *%s\. *%s$' % (year_pattern, issues_pattern, pages_pattern))),  # year.issue.pages
    # ('issue.year.pages', re.compile('^(?P<journal>[\w ]+?) *%s\. *%s. *%s$' % (issues_pattern, year_pattern, pages_pattern))),  # issue.year.pages
    # ('year.pages', re.compile('^(?P<journal>[\w ]+?) *%s. *%s$' % (year_pattern, pages_pattern))),  # year.pages
]
reference_patterns.extend(
    [('journal', re.compile('^' + journal_pattern + ' *' + '\. *'.join(sub_patterns) + '$', re.UNICODE)) for
     sub_patterns in [
         (volume_pattern, issues_pattern, year_pattern, pages_pattern),
         (volume_pattern, issues_pattern, pages_pattern),
         (year_pattern, issues_pattern, pages_pattern),
         (volume_pattern, year_pattern, pages_pattern),
         (year_pattern, pages_pattern),
         (year_pattern,),
     ]],
)


def parse_reference(raw_reference):
    if not isinstance(raw_reference, str):
        return None
    raw_reference = raw_reference.strip('. ')
    for reference_type, reference_pattern in reference_patterns:
        reference_match = reference_pattern.search(raw_reference)
        if reference_match:
            group_dict = reference_match.groupdict()
            for key, value in list(group_dict.items())[:]:
                if value is None:
                    del group_dict[key]
                    continue
                if value.isdigit():
                    if key == 'yearEnd' and len(value) == 2:
                        value = str(group_dict['yearStart'])[:2] + value
                    group_dict[key] = int(value)
            group_dict['type'] = reference_type
            group_dict['raw'] = raw_reference
            return group_dict or None


def parse_material(material):
    if not isinstance(material, str):
        return material
    match = re.match('(\d+) *(.+)', material)
    if not match:
        return material
    count = match.group(1)
    material_types = {
        '(?:Tab\.|Tabellen?|Tafeln?)': 'table',
        '(?:Karten?)': 'map',
        '(?:Falt(?:karten?|plan|pläne))': 'fold-up map',
        '(?:Falttabellen?)': 'fold-up table',
        '(?:Abb\.)': 'figure',
    }
    for type_pattern, type_name in material_types.items():
        if re.match(type_pattern, match.group(2)):
            break
        else:
            type_name = match.group(2)
    return {
        'count': int(count),
        'type': type_name,
        'raw': material,
    }


def parse_date_published(date_str: str):
    if date_str and date_str.isdigit():
        return {
            'year': int(date_str)
        }
    return None


def parse_date(date_str):
    if not isinstance(date_str, str):
        return date_str

    match = re.match(
        '(?:(\d{1,2})\. *(?:([IVX]{1,4})\. *)?(\d{4})?[-—])?(\d{1,2})\. *([IVX]{1,4})\. *(\d{4})',
        date_str
    )

    if match:
        roman_numerals = ('i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii')
        day_end = int(match.group(4))
        month_end = roman_numerals.index(match.group(5).lower()) + 1
        year_end = int(match.group(6))

        day_start = int(match.group(1)) if match.group(1) else day_end
        month_start = roman_numerals.index(match.group(2).lower()) + 1 if match.group(2) else month_end
        year_start = int(match.group(3)) if match.group(3) else year_end

        try:
            date_start = datetime(year_start, month_start, day_start).isoformat()
        except ValueError:
            print([year_start, month_start, day_start])
            date_start = None
        try:
            date_end = datetime(year_end, month_end, day_end)
        except ValueError:
            date_end = None

        return {
            'start': date_start,
            'end': date_end,
            'raw': date_str,
        }
