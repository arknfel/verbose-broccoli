from abc import abstractmethod
from common.root_aggregate import Actor


class Logger(Actor):
    @abstractmethod
    def debug(self): ...

    @abstractmethod
    def info(self): ...

    @abstractmethod
    def warn(self): ...

    @abstractmethod
    def error(self): ...
