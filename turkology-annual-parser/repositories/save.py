import logging
import os
from typing import List

from domain.citation import Citation
from repositories.JsonRepository import JsonRepository


def save_citations(citations: List[Citation], output_filename: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_filename)), exist_ok=True)
    repository = JsonRepository(output_filename)
    logging.info('Writing JSON file...')
    repository.write_citations(citations)
