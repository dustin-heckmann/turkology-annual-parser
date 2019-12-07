import logging

import bson
import pymongo


class MongoRepository(object):
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

    def citation(self, volume=None, number=None, id=None, version=None):
        if id:
            citation = self._citations.find_one({'_id': bson.ObjectId(id)})
        elif None in (volume, number):
            raise ValueError('You must specify either an id or a volume and entry number')
        else:
            search_dict = {'volume': volume, 'number': number}
            citations = list(self._citations.find(search_dict).sort([('_version', pymongo.DESCENDING)]))
            if version:
                version = int(version)
            else:
                version = citations[0]['_version']
            citation = citations[-version]
            citations.remove(citation)
            for historic_citation in citations:
                for attribute in list(historic_citation.keys()):
                    if not attribute.startswith('_'):
                        del historic_citation[attribute]
            citation['_versionHistory'] = citations
        if not citation:
            raise LookupError('Citation with id %s not found', id)
        citation['id'] = id
        return citation

    def citations(self, query=None, limit=0, skip=0, order_fields=None, fullyParsed=None, obsolete=False):
        if query is None:
            criteria = {}
        else:
            criteria = {'$text': {'$search': query}}
        if fullyParsed is not None:
            criteria['fullyParsed'] = fullyParsed
        if not obsolete:
            criteria['_obsolete'] = {'$ne': True}
        projections = None
        if order_fields:
            order_fields = [(field_name, {True: pymongo.ASCENDING, False: pymongo.DESCENDING}[ascending]) for
                            field_name, ascending in order_fields]
        else:
            if query:
                order_fields = (('score', {'$meta': 'textScore'}),)
                projections = {'score': {'$meta': "textScore"}}
            else:
                order_fields = (('volume', pymongo.ASCENDING), ('number', pymongo.ASCENDING))

        if projections:
            citations = self._citations.find(criteria, projections)
        else:
            citations = self._citations.find(criteria)
        return {
            'data': list(citations.sort(order_fields).skip(skip).limit(limit)),
            'total': self._citations.count(criteria),
        }

    def count_citations(self, criteria=None):
        criteria = criteria or {}
        return self._citations.count(criteria)

    def volumes(self):
        return self._citations.distinct("volume")  # .sort([('volume', pymongo.ASCENDING)])

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
