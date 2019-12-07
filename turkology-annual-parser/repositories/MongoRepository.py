import logging

import pymongo

from repositories.Repository import Repository


class MongoRepository(Repository):
    def __init__(self, host=None, port=None, db=None):
        database = pymongo.MongoClient(host, port)[db]
        logging.info({'host': host, 'port': port, 'db': db})
        self._paragraphs = database['paragraphs']
        self._citations = database['citations']
        self._create_indexes()

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
        self._citations.insert_many(citations)

    def insert_citation(self, citation):
        if '_id' in citation:
            self._citations.update({'_id': citation['_id']}, {'$set': {'_obsolete': True}})
            del citation['_id']
        self._citations.update({'volume': citation['volume'], 'number': citation['number']},
                               {'$set': {'_obsolete': True}})
        self._citations.insert_one(citation)

    def insert_paragraphs(self, paragraphs):
        self._paragraphs.insert_many(paragraphs)

    def distinct_author_names(self):
        return set([author.strip().lower() for author in self._citations.distinct('authors.raw') if author])

    def citations_with_missing_author(self):
        return self._citations.find({'authors': None, 'fullyParsed': False, '_obsolete': {'$ne': True}})

    def all_citations(self):
        return self._citations.find({'_obsolete': {'$ne': True}})

    def delete_all_data(self):
        self._paragraphs.drop()
        self._citations.drop()
