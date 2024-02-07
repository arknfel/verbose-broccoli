from common.interfaces import Repository
from .error import MemoryRepositoryError


class DictRepository(Repository):
    error_type = MemoryRepositoryError

    def __init__(self, data: dict):
        self.data = {**data}

    def get(self, _id, default=None):
        return self.data.get(_id, default)