from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticSearchRepository(object):
    def __init__(self):
        self._es = Elasticsearch(hosts=['localhost:9200'])
        self._es.indices.create(index='citations', ignore=[400, 403])

    def delete_all_data(self):
        self._es.delete_by_query('citations', body={'query': {'match_all': {}}})

    def insert_citations(self, citations):
        citations = map(lambda citation: {
            '_index': 'citations',
            '_type': 'citation',
            **convert_citation(citation)}, citations)
        bulk(self._es, citations, chunk_size=1000, request_timeout=200)


def convert_citation(citation):
    if citation.get('_id'):
        citation['id'] = str(citation['_id'])
        del citation['_id']
    del citation['_version']
    return citation
