from abc import abstractmethod

from common.root_aggregate.entity import Entity


# class RepositoryError(Entity.error): ...


class Repository(Entity):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def get(self, _id): ...

    @abstractmethod
    def put(self, _id, value): ...
