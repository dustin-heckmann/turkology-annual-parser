# -*- coding: utf-8 -*-
from dataclasses import replace

from paragraph.wmlparser import WMLParser


def extract_paragraphs(volume_filename):
    volume_number = volume_from_filename(volume_filename)
    parser = WMLParser(volume_filename)
    for paragraph in parser:
        yield replace(paragraph, volume=volume_number)


def volume_from_filename(volume_filename: str) -> int:
    volume_number = volume_filename.split("/")[-1].split("_")[0][2:]
    return int(volume_number.split('-')[0])
