# -*- coding: utf-8 -*-
import re
from dataclasses import replace
from operator import attrgetter
from typing import Iterable

from domain.paragraph import Paragraph


def replace_text(search_pattern, replacement, paragraph: Paragraph):
    return replace(paragraph, text=re.sub(search_pattern, replacement, paragraph.text))


def split_paragraph_before(paragraph: Paragraph, split_str):
    text = paragraph.text
    paragraph = replace(paragraph, text='')
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


def correct_paragraphs(paragraphs: Iterable[Paragraph]) -> Iterable[Paragraph]:
    paragraphs = list(paragraphs)
    volume = paragraphs[0].volume
    if volume == 1:
        correct_volume_1(paragraphs)
    elif volume == 2:
        correct_volume_2(paragraphs)
    elif volume == 3:
        paragraphs = correct_volume_3(paragraphs)
    elif volume == 4:
        correct_volume_4(paragraphs)
    elif volume == 5:
        correct_volume_5(paragraphs)
    elif volume == 6:
        paragraphs = correct_volume_6(paragraphs)
    elif volume == 7:
        paragraphs = correct_volume_7(paragraphs)
    elif volume == 8:
        paragraphs = correct_volume_8(paragraphs)
    elif volume == 9:
        paragraphs = correct_volume_9(paragraphs)
    elif volume == 10:
        paragraphs = correct_volume_10(paragraphs)
    elif volume == 11:
        paragraphs = correct_volume_11(paragraphs)
    elif volume == 12:
        correct_volume_12(paragraphs)
    elif volume == 13:
        correct_volume_13(paragraphs)
    elif volume == 15:
        correct_volume_15(paragraphs)
    elif volume == 16:
        paragraphs = correct_volume_16(paragraphs)
    elif volume == 18:
        correct_volume_18(paragraphs)
    elif volume == 19:
        correct_volume_19(paragraphs)
    elif volume == 20:
        correct_volume_20(paragraphs)
    elif volume == 21:
        paragraphs = correct_volume_21(paragraphs)
    elif volume == 22:
        paragraphs = correct_volume_22(paragraphs)
    elif volume == 24:
        paragraphs = correct_volume_24(paragraphs)
    elif volume == 25:
        paragraphs = correct_volume_25(paragraphs)
    return filter(lambda x: x is not None, paragraphs)


def correct_volume_25(paragraphs):
    paragraphs = flatten_list([
        paragraphs[:3771],
        [merge_paragraphs([
            paragraphs[3771],
            replace_text(r'1992\..*', '', paragraphs[3775])
        ])],
        paragraphs[3772:3775],
        [replace_text(r'^.+?1992\.', '1992.', paragraphs[3775])],
        paragraphs[3776:]
    ])
    return paragraphs


def correct_volume_24(paragraphs):
    paragraphs[3498] = merge_paragraphs([paragraphs[3498], paragraphs[3502]])
    empty_paragraphs(paragraphs, 3502, 3503)

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
    return paragraphs


def correct_volume_22(paragraphs):
    paragraphs = flatten_list([
        paragraphs[:1161],
        [replace_text('^542·', '542.', paragraphs[1161])],
        paragraphs[1162:4663],
        [replace_text('^ι 2615', '2615', paragraphs[4663])],
        paragraphs[4664:6084],
        paragraphs[6124:]
    ])
    return paragraphs


def correct_volume_21(paragraphs):
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
    return paragraphs


def correct_volume_20(paragraphs):
    empty_paragraphs(paragraphs, 2041, 2056)


def correct_volume_19(paragraphs):
    paragraphs[3081] = replace_text('^Î48L', '1481.', paragraphs[3081])

    paragraphs[1838] = merge_paragraphs(paragraphs[1838:1840])
    empty_paragraphs(paragraphs, 1839, 1840)

    paragraphs[1842] = merge_paragraphs(paragraphs[1842:1844])
    empty_paragraphs(paragraphs, 1843, 1844)

    paragraphs[3447] = merge_paragraphs([paragraphs[3447], paragraphs[3450]])
    empty_paragraphs(paragraphs, 3450, 3451)


def correct_volume_18(paragraphs):
    paragraphs[2997] = merge_paragraphs(paragraphs[2997:2999])
    empty_paragraphs(paragraphs, 2998, 2999)

    paragraphs[3286] = merge_paragraphs(paragraphs[3286:3288])
    empty_paragraphs(paragraphs, 3287, 3288)

    paragraphs[3288] = merge_paragraphs(paragraphs[3288:3290])
    empty_paragraphs(paragraphs, 3289, 3290)


def correct_volume_16(paragraphs):
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
    return paragraphs


def correct_volume_15(paragraphs):
    paragraphs[1890] = merge_paragraphs(paragraphs[1890:1892])
    empty_paragraphs(paragraphs, 1891, 1892)

    paragraphs[1900] = merge_paragraphs(paragraphs[1900:1902])
    empty_paragraphs(paragraphs, 1901, 1902)


def correct_volume_13(paragraphs):
    empty_paragraphs(paragraphs, 1404, 1425)
    empty_paragraphs(paragraphs, 4287, 4312)
    empty_paragraphs(paragraphs, 4382, 4407)


def correct_volume_12(paragraphs):
    empty_paragraphs(paragraphs, 2249, 2274)
    empty_paragraphs(paragraphs, 3140, 3158)
    empty_paragraphs(paragraphs, 3158, 3177)


def correct_volume_11(paragraphs):
    empty_paragraphs(paragraphs, 2007, 2032)
    empty_paragraphs(paragraphs, 2219, 2242)
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
    return paragraphs


def correct_volume_10(paragraphs):
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
            ''.join((
                '^í    f    · ',
                'Die Wirkung der Persönlichkeit Atatürks in der Dritten Welt, s. V ,>        ',
            )),
            '• Die Wirkung der Persönlichkeit Atatürks in der Dritten Welt, s.',
            paragraphs[4777]
        )],
        split_paragraph_before(
            replace_text(r'^.+?462\.',
                         '• Der Einfluß der osmanischen Kalligraphie in Europa, s. 2107 2462.',
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
    return paragraphs


def correct_volume_9(paragraphs):
    empty_paragraphs(paragraphs, 2460, 2496)
    empty_paragraphs(paragraphs, 2538, 2559)

    paragraphs[3885] = merge_paragraphs(paragraphs[3885:3887])
    empty_paragraphs(paragraphs, 3886, 3887)

    paragraphs[3899] = merge_paragraphs(paragraphs[3899:3901])
    empty_paragraphs(paragraphs, 3900, 3901)

    paragraphs[1519] = merge_paragraphs(paragraphs[1519:1521])
    empty_paragraphs(paragraphs, 1520, 1521)

    paragraphs[1521] = merge_paragraphs(paragraphs[1521:1523])
    empty_paragraphs(paragraphs, 1522, 1523)

    paragraphs = flatten_list([
        paragraphs[:980],
        [replace_text(r"^' ", '', paragraphs[980])],
        paragraphs[981:3350],
        split_paragraph_before(paragraphs[3350], '1605.'),
        split_paragraph_before(paragraphs[3351], '1606.'),
        paragraphs[3352:]
    ])
    return paragraphs


def correct_volume_8(paragraphs):
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
    return paragraphs


def correct_volume_7(paragraphs):
    empty_paragraphs(paragraphs, 3571, 3594)
    empty_paragraphs(paragraphs, 3620, 3646)
    empty_paragraphs(paragraphs, 4417, 4435)

    paragraphs[1773] = merge_paragraphs([paragraphs[1773], paragraphs[1777]])
    empty_paragraphs(paragraphs, 1777, 1778)

    paragraphs[4240] = merge_paragraphs([paragraphs[4240], paragraphs[4243]])
    empty_paragraphs(paragraphs, 4243, 4244)

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
    return paragraphs


def correct_volume_6(paragraphs):
    empty_paragraphs(paragraphs, 2868, 2885)
    empty_paragraphs(paragraphs, 3643, 3662)
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
    return paragraphs


def correct_volume_5(paragraphs):
    empty_paragraphs(paragraphs, 844, 845)
    empty_paragraphs(paragraphs, 3289, 3306)
    empty_paragraphs(paragraphs, 4342, 4362)
    paragraphs[1281] = replace_text('^521ï', '521.', paragraphs[1281])
    paragraphs[1661] = None
    paragraphs[2076] = replace_text('^1048', '1048.', paragraphs[2076])

    paragraphs[2705] = merge_paragraphs(paragraphs[2705:2707])
    empty_paragraphs(paragraphs, 2706, 2707)

    paragraphs[3510] = merge_paragraphs([paragraphs[3510], paragraphs[3513]])
    empty_paragraphs(paragraphs, 3511, 3512)

    paragraphs[3771] = replace_text('^2076', '2067', paragraphs[3771])
    paragraphs[4032] = replace_text('^2119', '2219', paragraphs[4032])


def correct_volume_4(paragraphs):
    empty_paragraphs(paragraphs, 1728, 1748)
    empty_paragraphs(paragraphs, 3127, 3152)

    paragraphs[1971] = merge_paragraphs(paragraphs[1971:1973])
    empty_paragraphs(paragraphs, 1972, 1973)

    paragraphs[4273] = merge_paragraphs(paragraphs[4273:4275])
    empty_paragraphs(paragraphs, 4274, 4275)


def correct_volume_3(paragraphs):
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
    return paragraphs


def correct_volume_2(paragraphs):
    paragraphs[2024] = merge_paragraphs([paragraphs[2024], paragraphs[2028], paragraphs[2029]])
    paragraphs[2028] = paragraphs[2029] = None

    paragraphs[2035] = merge_paragraphs(paragraphs[2035:2037])
    paragraphs[2036] = None

    paragraphs[3088] = merge_paragraphs(paragraphs[3088:3090])
    del paragraphs[3089]


def correct_volume_1(paragraphs):
    empty_paragraphs(paragraphs, 779, 798)  # duplicate page
    empty_paragraphs(paragraphs, 1912, 1932)  # duplicate page
    empty_paragraphs(paragraphs, 2306, 2324)  # duplicate page


def merge_paragraphs(paragraphs):
    return Paragraph(
        volume=paragraphs[0].volume,
        text=' '.join(map(attrgetter('text'), paragraphs)),
    )
