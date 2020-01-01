# -*- coding: utf-8 -*-
import re
from dataclasses import replace
from operator import attrgetter
from typing import List

from paragraph.paragraph import Paragraph


def replace_text(search_pattern, replacement, paragraph: Paragraph):
    return replace(paragraph, text=re.sub(search_pattern, replacement, paragraph.text))


def split_paragraph_before(paragraph: Paragraph, split_str):
    text = paragraph.text
    paragraph.text = None
    split_index = text.index(split_str)
    if split_index == -1:
        return [paragraph]

    def create_paragraph(text):
        return replace(paragraph, text=text)

    return [
        create_paragraph(text=text[:split_index]),
        create_paragraph(text=text[split_index:])
    ]


def flatten_list(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def empty_paragraphs(paragraphs, lower_bound, upper_bound):
    for i in range(lower_bound, upper_bound):
        paragraphs[i] = None


def correct_paragraphs(paragraphs: List[Paragraph]):
    volume = paragraphs[0].volume
    if volume == 1:
        empty_paragraphs(paragraphs, 779, 798)  # duplicate page
        empty_paragraphs(paragraphs, 1912, 1932)  # duplicate page
        empty_paragraphs(paragraphs, 2306, 2324)  # duplicate page
    elif volume == 2:
        paragraphs[3088] = merge_paragraphs(paragraphs[3088:3090])
        del paragraphs[3089]
    elif volume == 3:
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
    elif volume == 4:
        empty_paragraphs(paragraphs, 1728, 1748)
        empty_paragraphs(paragraphs, 3127, 3152)
    elif volume == 5:
        empty_paragraphs(paragraphs, 3289, 3306)
        empty_paragraphs(paragraphs, 4342, 4362)
        paragraphs[1281] = replace_text('^521ï', '521.', paragraphs[1281])
        paragraphs[2076] = replace_text('^1048', '1048.', paragraphs[2076])
        paragraphs[3771] = replace_text('^2076', '2067', paragraphs[3771])
        paragraphs[4032] = replace_text('^2119', '2219', paragraphs[4032])
    elif volume == 6:
        empty_paragraphs(paragraphs, 2868, 2885)
        empty_paragraphs(paragraphs, 4916, 4933)
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
    elif volume == 7:
        empty_paragraphs(paragraphs, 3571, 3594)
        empty_paragraphs(paragraphs, 3620, 3646)
        empty_paragraphs(paragraphs, 4417, 4435)
        paragraphs = flatten_list([
            paragraphs[:2446],
            [replace_text('^.1245. LlU', '1245. Liu', paragraphs[2446])],
            paragraphs[2447:2668],
            [replace_text(r'^lóét\)', '1376', paragraphs[2668])],
            paragraphs[2669:2675],
            [replace_text(r'^« +', '', paragraphs[2675])],
            paragraphs[2676:2970],
            [replace_text(r'^\. ', '', paragraphs[2970])],
            paragraphs[2971:4123],
            [replace_text(r'^2196:', '2196.', paragraphs[4123])],
            paragraphs[4124:]
        ])
    elif volume == 8:
        empty_paragraphs(paragraphs, 3161, 3181)
        paragraphs = flatten_list([
            paragraphs[:2381],
            split_paragraph_before(
                replace_text(r'İ230\.', '1230.', paragraphs[2381]),
                '1230.'
            ),
            paragraphs[2382:2416],
            [replace_text('^1250verol', '1250. Erol', paragraphs[2416])],
            paragraphs[2417:2557],
            split_paragraph_before(
                replace_text(r'^.+laque ur', '1330. Laqueur', paragraphs[2557]),
                '1331.'
            ),
            paragraphs[2558:3749],
            [replace_text(r'^.+?3\.', '2083.', paragraphs[3749])],
            paragraphs[3750:]
        ])
    elif volume == 9:
        empty_paragraphs(paragraphs, 2460, 2496)
        empty_paragraphs(paragraphs, 2538, 2559)
        paragraphs = flatten_list([
            paragraphs[:980],
            [replace_text(r"^' ", '', paragraphs[980])],
            paragraphs[981:3350],
            split_paragraph_before(paragraphs[3350], '1605.'),
            split_paragraph_before(paragraphs[3351], '1606.'),
            paragraphs[3352:]
        ])
    elif volume == 10:
        empty_paragraphs(paragraphs, 1008, 1029)
        empty_paragraphs(paragraphs, 1071, 1091)
        empty_paragraphs(paragraphs, 3388, 3408)
        empty_paragraphs(paragraphs, 4575, 4595)
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
    elif volume == 11:
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
    elif volume == 16:
        paragraphs = flatten_list([
            paragraphs[:349],
            [replace_text(
                '^I.\t.',
                '1. ',
                merge_paragraphs(paragraphs[349:351])
            )],
            paragraphs[351:361],
            [replace_text('^II.\t', '11. ', paragraphs[361])],
            paragraphs[361:463],
            split_paragraph_before(
                replace_text(
                    '70.. TARDY',
                    '70.\tTARDY',
                    merge_paragraphs(paragraphs[463:465])
                ),
                '70.'
            ),
            paragraphs[465:]
        ])
    elif volume == 19:
        paragraphs[3081] = replace_text('^Î48L', '1481.', paragraphs[3081])
    elif volume == 21:
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
            [replace_text(
                '^12Ì0',
                '1210',
                paragraphs[2617]
            )],
            paragraphs[2618:]
        ])
    elif volume == 22:
        paragraphs = flatten_list([
            paragraphs[:1161],
            [replace_text('^542·', '542.', paragraphs[1161])],
            paragraphs[1162:4663],
            [replace_text('^ι 2615', '2615', paragraphs[4663])],
            paragraphs[4664:6084],
            paragraphs[6124:]
        ])
    elif volume == 24:
        paragraphs = flatten_list([
            paragraphs[:726],
            [replace_text(' 262;.*', '', merge_paragraphs(paragraphs[726:729]))],
            [replace_text('^.+?262;', '262.', merge_paragraphs(paragraphs[728:731]))],
            paragraphs[731:786],
            split_paragraph_before(paragraphs[786], '290.'),
            paragraphs[787:2817],
            [replace_text('1535;.+$', '', paragraphs[2817])],
            [replace_text('^.+1535;', '1535.', paragraphs[2817])],
            paragraphs[2818:4497],
            split_paragraph_before(
                replace_text(
                    '^2516;', '2516.',
                    merge_paragraphs(paragraphs[4497:4501])
                ),
                '2517.'
            ),
            paragraphs[4501:4627],
            [replace_text('^2588;', '2588.', paragraphs[4627])],
            [paragraphs[4628]],
            [replace_text('^2589;', '2589.', paragraphs[4629])],
            paragraphs[4630:4911],
            [replace_text('^llľò. yusuf Has HacÍB', '2773. Yusuf Has Hacib', paragraphs[4911])],
            split_paragraph_before(paragraphs[4912], '2774.'),
            paragraphs[4913:]
        ])
    elif volume == 25:
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
    return filter(lambda x: x is not None, paragraphs)


def merge_paragraphs(paragraphs):
    return Paragraph(
        volume=paragraphs[0].volume,
        text=' '.join(map(attrgetter('text'), paragraphs)),
    )
