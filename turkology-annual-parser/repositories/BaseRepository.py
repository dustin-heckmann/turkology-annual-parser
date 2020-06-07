from abc import ABCMeta, abstractmethod
from dataclasses import asdict, replace

from domain.citation import Citation


class BaseRepository(object):
    __meta__ = ABCMeta

    @abstractmethod
    def write_citations(self, citations):
        pass

    @classmethod
    def _citation_as_dict(cls, citation: Citation):
        citation_dict = asdict(
            replace(citation, type=citation.type.value if citation.type else None),
            dict_factory=cls._to_dict
        )
        citation_dict['fullyParsed'] = citation.fully_parsed()
        return citation_dict

    @classmethod
    def _to_dict(cls, it):
        return dict(
            [
                (cls.to_camel_case(key), value)
                for key, value in it
                if value
            ]
        )

    @staticmethod
    def to_camel_case(snake_str):
        components = snake_str.split('_')
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
        return components[0] + ''.join(x.title() for x in components[1:])
