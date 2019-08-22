# -*- coding: utf-8 -*-
from operator import itemgetter


def correct_paragraphs(paragraphs):
    volume = paragraphs[0]['volume']
    if volume == '2':
        paragraphs[3088] = merge_paragraphs(paragraphs[3088:3090])
        del paragraphs[3089]
    elif volume == '3':
        paragraphs = paragraphs[:700] + [merge_paragraphs(paragraphs[701:707])] + paragraphs[707:]
    return paragraphs


def merge_paragraphs(paragraphs):
    return {
        'mergedFrom': list(map(itemgetter('originalIndex'), paragraphs)),
        'volume': paragraphs[0]['volume'],
        'text': ' '.join(map(itemgetter('text'), paragraphs)),
    }
