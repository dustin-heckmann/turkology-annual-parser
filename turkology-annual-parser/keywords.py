import csv
from typing import Dict


def get_keyword_mapping(file_name: str) -> Dict[str, Dict[str, str]]:
    with open(file_name, encoding='utf-8') as keyword_file:
        reader = csv.reader(keyword_file, delimiter=';', quotechar='"')
        keyword_mapping = {
            code: {'de': name_de, 'en': name_en}
            for (code, name_de, name_en) in reader
        }
        return keyword_mapping
