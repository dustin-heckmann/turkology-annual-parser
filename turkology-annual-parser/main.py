import argparse
import csv
import logging
import multiprocessing
import os
from multiprocessing.queues import Queue
from typing import Dict, List, Set

from citation.assembly import assemble_citations
from citation.citation_parsing import find_known_authors, parse_citation
from citation.field_parsing import parse_citation_fields
from citation.id_assignment import assign_citation_ids
from citation.keywords import normalize_keywords_for_citation
from compression import create_zip_file
from domain.citation import Citation
from paragraph.paragraph_correction import correct_paragraphs
from paragraph.paragraph_extraction import extract_paragraphs
from paragraph.type_detection import detect_paragraph_types
from repetitions.repetitions import resolve_repetitions
from repositories.JsonRepository import JsonRepository


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='*', help='Location of OCR directory', required=True)
    parser.add_argument('--output', '-o', help='Location of JSON output file', required=True)
    parser.add_argument(
        '--zip-output', '-z', help='Location of compressed export bundle', required=True
    )
    parser.add_argument('--keyword-file', help='Path to keyword CSV', required=True)
    parser.add_argument('--find-authors', action='store_true')
    parser.add_argument('--resolve-repetitions', action='store_true')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args()
    setup_logging(args.verbose)

    citations = run_full_pipeline(args.input, args.keyword_file)

    if args.find_authors:
        citations = find_authors(citations)
    if args.resolve_repetitions:
        citations = resolve_repetitions(citations)
    save_citations(citations, args.output)
    create_export_bundle(args.output, args.zip_output)


HARDCODED_AUTHORS = {
    'Condurachi, Em',
    'Kakük, Z',
    'Yoman, Yakut',
    'Kobeneva, T. A',
    'Djukanovic, Marija',
    'Zagorka Janc',
    'Sohbweide, Hanna',
    'Tübkay, Cevdet',
    'Eren, ismail',
    'Baysal,   Jale',
    'Spiridonakis, B. G',
    'Uçankuş, Hasan T',
    'Landau, Jacob M',
    'Özeğe, Seyfettin',
}


def find_authors(citations: List[Citation]):
    known_authors = get_known_authors_from_citations(citations)
    known_authors.update(HARDCODED_AUTHORS)
    logging.info('Found {} distinct authors'.format(len(known_authors)))
    return find_known_authors(citations, known_authors)


def get_known_authors_from_citations(citations: List[Citation]) -> Set[str]:
    known_authors = set()
    for citation in citations:
        for author in citation.authors:
            if author.raw:
                known_authors.add(author.raw)
    return known_authors


def save_citations(citations: List[Citation], output_filename: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(output_filename)), exist_ok=True)
    repository = JsonRepository(output_filename)
    logging.info('Writing JSON file...')
    repository.write_citations(citations)


def run_full_pipeline(
        ocr_files: List[str],
        keyword_file: str
) -> List[Citation]:
    keyword_mapping = get_keyword_mapping(keyword_file)
    m = multiprocessing.Manager()
    queue = m.Queue()
    with multiprocessing.Pool() as pool:
        args = ((volume_filename, keyword_mapping, queue) for volume_filename in ocr_files)
        pool.starmap(
            run_full_pipeline_on_volume,
            args
        )
    pool.join()
    citations = []
    while not queue.empty():
        citations.append(queue.get())
    pool.close()
    return citations


def run_full_pipeline_on_volume(
        volume_filename: str,
        keyword_mapping: Dict[str, Dict[str, str]],
        queue: Queue
) -> None:
    logging.info("START: %s", volume_filename)

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
    logging.info('DONE: %s', volume_filename)


def get_keyword_mapping(file_name: str) -> Dict[str, Dict[str, str]]:
    with open(file_name, encoding='utf-8') as keyword_file:
        reader = csv.reader(keyword_file, delimiter=';', quotechar='"')
        keyword_mapping = {code: {'de': name_de, 'en': name_en} for (code, name_de, name_en) in
                           reader}
        return keyword_mapping


def setup_logging(verbose: bool):
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(processName)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/tmp/ta_processing.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if verbose else logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(processName)s] %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


def create_export_bundle(dump_file_name: str, zip_path: str):
    logging.info('Writing export bundle...')
    create_zip_file([dump_file_name, dump_file_name + 'l'], zip_path)


if __name__ == '__main__':
    main()
