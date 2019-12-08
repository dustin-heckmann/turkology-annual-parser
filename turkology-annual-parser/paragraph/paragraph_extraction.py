# -*- coding: utf-8 -*-
from dataclasses import replace

from paragraph.wmlparser import WMLParser


def extract_paragraphs(volume_filename):
    volume_number = extract_volume_from_filename(volume_filename)
    parser = WMLParser(volume_filename)
    for paragraph in parser:
        yield replace(paragraph, volume=volume_number)


def extract_volume_from_filename(volume_filename):
    volume_number = volume_filename.split("/")[-1].split("_")[0][2:]
    return str(int(volume_number)) if volume_number.isdigit() else volume_number
