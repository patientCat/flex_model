from abc import abstractmethod


class MetaColumn:
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def format(self):
        pass

    @abstractmethod
    def type(self):
        pass
