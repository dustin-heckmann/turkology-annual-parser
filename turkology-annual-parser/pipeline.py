import logging
import multiprocessing
import os
from queue import Queue
from typing import List, Dict

from bootstrap.authors import reparse_citations_using_known_authors
from citation.assembly import assemble_citations
from citation.citation_parsing import parse_citation
from citation.field_parsing import parse_citation_fields
from citation.id_assignment import assign_citation_ids
from citation.keywords import normalize_keywords_for_citation
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

    logging.info(f'Parsing {len(ocr_files)} volumes...')
    m = multiprocessing.Manager()
    queue = m.Queue()
    with multiprocessing.Pool() as pool:
        args = ((volume_filename, keyword_mapping, queue) for volume_filename in ocr_files)
        pool.starmap(run_full_pipeline_on_volume, args)
    pool.join()
    citations = []
    while not queue.empty():
        citations.append(queue.get())
    pool.close()

    if find_authors:
        logging.info('Bootstrapping known authors...')
        citations = reparse_citations_using_known_authors(citations)
    if resolve_repetitions:
        logging.info('Resolving repetitions...')
        citations = extend_citations_with_later_added_info(citations)
    return citations


def run_full_pipeline_on_volume(
        volume_filename: str,
        keyword_mapping: Dict[str, Dict[str, str]],
        queue: Queue
) -> None:
    logging.debug('Extracting paragraphs...')
    paragraphs = list(extract_paragraphs(volume_filename))

    logging.debug('Performing paragraph corrections...')
    paragraphs = correct_paragraphs(paragraphs)

    logging.debug('Determining paragraph types...')
    typed_paragraphs = list(detect_paragraph_types(paragraphs, keyword_mapping))

    logging.debug('Assembling citations...')
    raw_citations = assemble_citations(typed_paragraphs)

    logging.debug('Parsing citations...')
    intermediate_citations = (parse_citation(citation) for citation in raw_citations)
    citations = (parse_citation_fields(citation) for citation in intermediate_citations)
    citations = assign_citation_ids(citations)
    citations = (normalize_keywords_for_citation(citation, keyword_mapping) for citation in
                 citations)
    for citation in citations:
        queue.put(citation)
    logging.info(f'{os.path.basename(volume_filename)} [DONE]')
