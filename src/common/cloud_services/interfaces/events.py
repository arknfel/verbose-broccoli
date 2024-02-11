from abc import abstractmethod

from .. import Service


class Events(Service):
    @abstractmethod
    def create(self): ...

    @abstractmethod
    def delete(self): ...

    @abstractmethod
    def update(self): ...
