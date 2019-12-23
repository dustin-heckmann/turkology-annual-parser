import logging
from dataclasses import asdict, replace

import pymongo

from repositories.Repository import Repository


class MongoRepository(Repository):
    def __init__(self, host=None, port=None, db=None):
        database = pymongo.MongoClient(host, port)[db]
        logging.info({'host': host, 'port': port, 'db': db})
        self._citations = database['citations']

    def _create_indexes(self):
        logging.info('Creating indexes...')
        self._citations.create_index([('volume', 1)])
        self._citations.create_index([('number', 1)])
        self._citations.create_index([('volume', 1), ('number', 1)])
        self._citations.create_index([('authors', 1)])
        self._citations.create_index([('fullyParsed', 1)])
        self._citations.create_index([('_obsolete', 1)])
        self._citations.create_index([
            ('rawText', 'text'),
            ('amendments', 'text'),
            ('keywords', 'text')]
        )

    def insert_citations(self, citations):
        self._citations.insert_many(
            (asdict(
                replace(citation, type=citation.type.value if citation.type else None), dict_factory=to_dict) for
            citation in citations
            )
        )
        self._create_indexes()

    def delete_all_data(self):
        self._citations.drop()


def to_dict(it):
    return dict(
        [
            (to_camel_case(key), value)
            for key, value in dict(it).items()
        ]
    )


def to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'title' method and join them together.
    return components[0] + ''.join(x.title() for x in components[1:])
