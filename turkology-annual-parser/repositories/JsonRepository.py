import json
from typing import Iterator, List

import jsonlines

from citation.citation import Citation
from repositories.BaseRepository import BaseRepository


class JsonRepository(BaseRepository):
    def __init__(self, filename):
        self._filename = filename

    def write_citations(self, citations: Iterator[Citation]):
        citations = [self._citation_as_dict(citation) for citation in citations]
        self._write_json(citations)
        self._write_json_lines(citations)

        with open(self._filename + 'l', 'w') as storage_file:
            writer = jsonlines.Writer(storage_file)
            for citation in citations:
                writer.write(citation)

    def _write_json(self, citations: List[Citation]):
        with open(self._filename, 'w') as storage_file:
            json.dump(
                citations,
                storage_file
            )

    def _write_json_lines(self, citations: List[Citation]):
        with jsonlines.open(self._filename + 'l', 'w') as writer:
            writer.write_all(citations)
