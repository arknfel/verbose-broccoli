from abc import abstractmethod

from common.root_aggregate import Entity


class RepositoryError(Entity.error_type): ...


class Repository(Entity):
    error_type = RepositoryError

    def __init__(self, data):
        self.repo = data

    @abstractmethod
    def get(self, _id): ...

    @abstractmethod
    def put(self, _id, value): ...
