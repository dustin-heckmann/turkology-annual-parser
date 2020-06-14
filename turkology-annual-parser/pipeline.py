import logging
import multiprocessing
import os
from functools import partial
from operator import attrgetter
from queue import Queue
from typing import List, Dict

from bootstrap.authors import reparse_citations_using_known_authors
from citation.assembly import assemble_citations
from citation.citation_parsing import parse_citations
from citation.field_parsing import parse_citation_fields
from citation.id_assignment import assign_citation_ids
from citation.keywords import normalize_keywords
from domain.citation import Citation
from keywords import get_keyword_mapping
from paragraph.paragraph_correction import correct_paragraphs
from paragraph.paragraph_extraction import extract_paragraphs
from paragraph.type_detection import detect_paragraph_types
from repetitions.repetitions import extend_citations_with_later_added_info


def run_pipeline(
        ocr_files: List[str],
        keyword_file: str,
        find_authors=False,
        resolve_repetitions=False
) -> List[Citation]:
    keyword_mapping = get_keyword_mapping(keyword_file)

    return pipeline(
        lambda: ocr_files,
        partial(run_isolated_pipelines_in_parallel, keyword_mapping=keyword_mapping),
        partial(sorted, key=attrgetter('volume')),
        find_authors and reparse_citations_using_known_authors,
        resolve_repetitions and extend_citations_with_later_added_info
    )


def run_isolated_pipelines_in_parallel(ocr_files: List[str], keyword_mapping):
    logging.info(f'Parsing {len(ocr_files)} volumes...')
    m = multiprocessing.Manager()
    queue = m.Queue()
    with multiprocessing.Pool() as pool:
        args = ((volume_filename, keyword_mapping, queue) for volume_filename in ocr_files)
        pool.starmap(run_isolated_pipeline_on_volume, args)
    pool.join()
    while not queue.empty():
        yield queue.get()
    pool.close()


def run_isolated_pipeline_on_volume(
        volume_filename: str,
        keyword_mapping: Dict[str, Dict[str, str]],
        queue: Queue
) -> None:
    for citation in pipeline(
            lambda: volume_filename,
            extract_paragraphs,
            correct_paragraphs,
            partial(detect_paragraph_types, keyword_mapping=keyword_mapping),
            assemble_citations,
            parse_citations,
            parse_citation_fields,
            assign_citation_ids,
            partial(normalize_keywords, keyword_mapping=keyword_mapping),
    ):
        queue.put(citation)
    logging.info(f'{os.path.basename(volume_filename)} [DONE]')


def pipeline(*steps):
    steps = filter(None, steps)  # Filter out falsy steps
    result = next(steps)()
    for step in steps:
        result = step(result)
    return result
