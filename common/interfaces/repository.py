from abc import abstractmethod

from common.root_aggregate import Entity
from .error import RepositoryError


class Repository(Entity):
    error_type = RepositoryError
    @abstractmethod
    def get(self, _id): ...

    @abstractmethod
    def put(self, _id, value): ...
