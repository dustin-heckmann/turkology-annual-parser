from abc import ABCMeta, abstractmethod


class Repository(object):
    __meta__ = ABCMeta

    @abstractmethod
    def insert_citations(self, citations):
        pass

    @abstractmethod
    def delete_all_data(self):
        pass
