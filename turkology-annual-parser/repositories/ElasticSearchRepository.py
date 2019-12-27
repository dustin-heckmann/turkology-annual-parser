import json
from dataclasses import asdict, replace
from os.path import join, dirname

from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import bulk

from citation.citation import Citation


class ElasticSearchRepository(object):
    def __init__(self, host=None, index=None):
        assert host is not None
        assert index is not None
        self._es = Elasticsearch(hosts=[f'{host}:9200'])
        self._index = index
        self._create_index()

    def _create_index(self):
        try:
            self._es.indices.delete(self._index)
        except NotFoundError:
            pass
        self.delete_all_data()
        with open(join(dirname(__file__), 'index_settings.json')) as settings_file:
            self._es.indices.create(index=self._index, body=json.load(settings_file))
        self._es.indices.put_settings(body={'max_result_window': 70000})

    def delete_all_data(self):
        try:
            self._es.delete_by_query(self._index, body={'query': {'match_all': {}}})
        except NotFoundError:
            pass

    def insert_citations(self, citations):
        citations = map(lambda citation: {
            '_index': self._index,
            '_type': 'citation',
            **self._citation_as_dict(citation)
        }, citations)
        bulk(self._es, citations, chunk_size=70000, request_timeout=200)

    @staticmethod
    def _citation_as_dict(citation: Citation):
        return asdict(
            replace(citation, type=citation.type.value if citation.type else None),
            dict_factory=to_dict
        )


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
