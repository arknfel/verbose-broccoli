from common.interfaces import Repository


class DictRepositoryError(Repository.error_type): ...


class DictRepository(Repository):
    error_type = DictRepositoryError

    def __init__(self, data: dict):
        self.data = {**data}

    def get(self, _id, default=None):
        return self.data.get(_id, default)

    def put(self, _id, value):
        self.data[_id] = value
