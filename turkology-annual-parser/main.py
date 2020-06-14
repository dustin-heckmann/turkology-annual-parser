import argparse
import logging

from export import create_export_bundle
from pipeline import run_pipeline
from repositories.save import save_citations


def main():
    args = parse_command_line_args()
    setup_logging(args.verbose)

    citations = run_pipeline(
        args.input,
        args.keyword_file,
        find_authors=args.find_authors,
        resolve_repetitions=args.resolve_repetitions
    )
    save_citations(citations, args.output)
    create_export_bundle(args.output, args.zip_output)


def parse_command_line_args():
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
    return args


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


if __name__ == '__main__':
    main()
