from abc import ABCMeta, abstractmethod


class Repository(object):
    __meta__ = ABCMeta

    @abstractmethod
    def insert_citations(self, citations):
        pass

    @abstractmethod
    def insert_citation(self, citation):
        pass

    @abstractmethod
    def insert_paragraphs(self, paragraphs):
        pass

    @abstractmethod
    def distinct_author_names(self):
        pass

    @abstractmethod
    def citations_with_missing_author(self):
        pass

    @abstractmethod
    def all_citations(self):
        pass

    @abstractmethod
    def delete_all_data(self):
        pass

