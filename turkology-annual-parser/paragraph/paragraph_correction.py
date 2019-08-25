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
        return dict(**paragraph, text=text)

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
        paragraphs = flatten_list([
            paragraphs[:461],
            [merge_paragraphs([paragraphs[461], paragraphs[465]])],
            paragraphs[462:465],
            paragraphs[466:2032],
            [replace_text('^895.0y', '895. Oy', paragraphs[2032])],
            paragraphs[2033:3339],
            [replace_text('^\\\\ 1609', '1609', paragraphs[3339])],
            paragraphs[3340:4275],
            split_paragraph_before(
                paragraphs[4275],
                '2161. Denham'
            ),
            paragraphs[4276:4775],
            [replace_text(
                r'Die 7.+?edenk', 'Die Gedenk',
                replace_text(r'^.+?461', '2461', paragraphs[4775])
            )],
            [replace_text(
                r'^.+$',
                '• Geheimverträge über die Aufteilung des Osmanischen Reiches, s. 628.',
                paragraphs[4776]
            )],
            [replace_text(
                r'^í    f    · Die Wirkung der Persönlichkeit Atatürks in der Dritten Welt, s. V ,>        ',
                '• Die Wirkung der Persönlichkeit Atatürks in der Dritten Welt, s.',
                paragraphs[4777]
            )],
            split_paragraph_before(
                replace_text(r'^.+?462\.', '• Der Einfluß der osmanischen Kalligraphie in Europa, s. 2107 2462.',
                             paragraphs[4778]),
                '2462.'
            ),
            paragraphs[4779:4837],
            [replace_text('^• 2505', '2505', paragraphs[4837])],
            paragraphs[4838:4844],
            [replace_text(
                'russi- sehe',
                'russische',
                merge_paragraphs([paragraphs[4844], paragraphs[4848]])
            )],
            paragraphs[4845:4848],
            paragraphs[4849:]
        ])
    elif volume == '11':
        paragraphs = flatten_list([
            paragraphs[:649],
            [replace_text(r'^\^209', '209', paragraphs[649])],
            split_paragraph_before(paragraphs[650], '210. Gil Grim'),
            paragraphs[651:2947],
            [merge_paragraphs(paragraphs[2947:2950])],
            paragraphs[2950:2979],
            [replace_text(r'^\.1561', '1561', paragraphs[2979])],
            paragraphs[2980:3822],
            [replace_text(r'^j2Ö6\|', '2061.', paragraphs[3822])],
            paragraphs[3823:],
        ])
    elif volume == '19':
        paragraphs[3081] = replace_text('^Î48L', '1481.', paragraphs[3081])
    elif volume == '21':
        paragraphs = flatten_list([
            paragraphs[:2180],
            split_paragraph_before(
                replace_text(
                    '#',
                    '',
                    merge_paragraphs(paragraphs[2180:2182]),
                ),
                '989.'
            ),
            paragraphs[2182:2617],
            replace_text(
                '^12Ì0',
                '1210',
                paragraphs[2617]
            ),
            paragraphs[2618:]
        ])
    elif volume == '25':
        paragraphs = flatten_list([
            paragraphs[:3771],
            [merge_paragraphs([
                paragraphs[3771],
                replace_text('1992\..*', '', paragraphs[3775])
            ])],
            paragraphs[3772:3775],
            [replace_text(r'^.+?1992\.', '1992.', paragraphs[3775])],
            paragraphs[3776:]
        ])
    return paragraphs


def merge_paragraphs(paragraphs):
    return {
        'volume': paragraphs[0]['volume'],
        'text': ' '.join(map(itemgetter('text'), paragraphs)),
    }
