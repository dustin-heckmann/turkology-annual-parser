# -*- coding: utf-8 -*-
import re
from operator import itemgetter


def replace_text(search_pattern, replacement, paragraph):
    paragraph = dict(**paragraph)
    paragraph['text'] = re.sub(search_pattern, replacement, paragraph['text'])
    return paragraph


def split_paragraph_before(paragraph, split_str):
    text = paragraph['text']
    del paragraph['text']
    split_index = text.index(split_str)
    if split_index == -1:
        return [paragraph]

    def create_paragraph(text):
        return dict(**paragraph, splitFrom=paragraph['originalIndex'], text=text)

    return [
        create_paragraph(text=text[:split_index]),
        create_paragraph(text=text[split_index:])
    ]


def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def correct_paragraphs(paragraphs):
    volume = paragraphs[0]['volume']
    if volume == '2':
        paragraphs[3088] = merge_paragraphs(paragraphs[3088:3090])
        del paragraphs[3089]
    elif volume == '3':
        before_1364, paragraph_1364 = split_paragraph_before(paragraphs[2589], '1364 Recueil')
        paragraph_1364 = replace_text('^1364', '1364.', paragraph_1364)

        paragraphs[627] = replace_text('^154', '154.', paragraphs[627])

        paragraphs = flatten_list([
            paragraphs[:700],
            [merge_paragraphs(paragraphs[701:707])],
            paragraphs[707:2589],
            [before_1364, paragraph_1364],
            paragraphs[2590:]
        ])
    elif volume == '5':
        paragraphs[1281] = replace_text('^521ï', '521.', paragraphs[1281])
        paragraphs[2076] = replace_text('^1048', '1048.', paragraphs[2076])
        paragraphs[3771] = replace_text('^2076', '2067', paragraphs[3771])
        paragraphs[4032] = replace_text('^2119', '2219', paragraphs[4032])
    elif volume == '6':
        paragraphs[1472] = replace_text('^63δ', '635', paragraphs[1472])
        paragraphs[2695] = replace_text('^J397', '1397', paragraphs[2695])
        paragraphs[3029] = replace_text('^Í596', '1596', paragraphs[3029])
        paragraphs = flatten_list([
            paragraphs[:1964],
            [merge_paragraphs([paragraphs[1964], paragraphs[1968]])],
            paragraphs[1965:1968],
            paragraphs[1969:]
        ]
        )
    elif volume == '10':
        paragraphs = paragraphs[:461] + [merge_paragraphs([paragraphs[461], paragraphs[465]])] + paragraphs[462:465] + paragraphs[466:]
    elif volume == '11':
        paragraphs = paragraphs[:2947] + [merge_paragraphs(paragraphs[2947:2950])] + paragraphs[2950:]
    elif volume == '19':
        paragraphs[3081] = replace_text('^Î48L', '1481', paragraphs[3081])
    return paragraphs


def merge_paragraphs(paragraphs):
    return {
        'mergedFrom': list(map(itemgetter('originalIndex'), paragraphs)),
        'volume': paragraphs[0]['volume'],
        'text': ' '.join(map(itemgetter('text'), paragraphs)),
    }
