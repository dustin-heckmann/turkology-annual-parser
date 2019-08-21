# -*- coding: utf-8 -*-

from paragraph.wmlparser import WMLParser


def extract_paragraphs(volume_filename):
    volume_number = volume_filename.split("/")[-1].split("_")[0][2:]
    if volume_number.isdigit():
        volume_number = str(int(volume_number))

    parser = WMLParser(volume_filename)
    for paragraph in parser.paragraphs:
        paragraph['volume'] = volume_number
        yield paragraph
