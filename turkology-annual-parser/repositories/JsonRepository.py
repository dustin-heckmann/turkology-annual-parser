import datetime
import json
from typing import Iterator

from citation.citation import Citation
from repositories.BaseRepository import BaseRepository


class JsonRepository(BaseRepository):
    def __init__(self, filename):
        self._filename = filename

    def write_citations(self, citations: Iterator[Citation]):
        with open(self._filename, 'w') as storage_file:
            json.dump(
                list(map(self._citation_as_dict, citations)),
                storage_file,
            )

