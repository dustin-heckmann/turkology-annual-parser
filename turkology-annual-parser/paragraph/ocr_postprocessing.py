# -*- coding: utf-8 -*-

import regex as re

broken_bullet_pattern = re.compile(r'^[φ#0Φ]\s+', re.UNICODE)


def postprocess_paragraph(paragraph):
    text = paragraph['text']
    if broken_bullet_pattern.match(text):
        return {
            **paragraph,
            'original_text': text,
            'text': '•' + text[1:],
        }
    return {**paragraph}
