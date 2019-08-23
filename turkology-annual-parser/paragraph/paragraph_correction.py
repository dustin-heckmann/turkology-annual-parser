# -*- coding: utf-8 -*-
from operator import itemgetter


def correct_paragraphs(paragraphs):
    volume = paragraphs[0]['volume']
    if volume == '2':
        paragraphs[3088] = merge_paragraphs(paragraphs[3088:3090])
        del paragraphs[3089]
    elif volume == '3':
        paragraphs = paragraphs[:700] + [merge_paragraphs(paragraphs[701:707])] + paragraphs[707:]
    elif volume == '6':
        paragraphs = paragraphs[:1964] + [merge_paragraphs([paragraphs[1964], paragraphs[1968]])] + paragraphs[1965:1968] + paragraphs[1969:]
    elif volume == '10':
        paragraphs = paragraphs[:461] + [merge_paragraphs([paragraphs[461], paragraphs[465]])] + paragraphs[462:465] + paragraphs[466:]
    elif volume == '11':
        paragraphs = paragraphs[:2947] + [merge_paragraphs(paragraphs[2947:2950])] + paragraphs[2950:]
    return paragraphs


def merge_paragraphs(paragraphs):
    return {
        'mergedFrom': list(map(itemgetter('originalIndex'), paragraphs)),
        'volume': paragraphs[0]['volume'],
        'text': ' '.join(map(itemgetter('text'), paragraphs)),
    }
