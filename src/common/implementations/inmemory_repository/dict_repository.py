from common.interfaces import Repository


class DictRepositoryError(Repository.error_type): ...


class DuplicateIdError(Exception):
    def __init__(self, _id, repo: 'DictRepository'):
        message = f"_id '{_id}' already exists in repo '{repo.__class__.__name__}'"
        super().__init__(message)


class DictRepository(Repository):
    error_type = DictRepositoryError

    def __init__(self, data: dict):
        self.data = {**data}

    def get(self, _id, default=None):
        return self.data.get(_id, default)

    def put(self, _id, value, overwrite=True):
        if not overwrite and _id in self.data:
            raise self.error_type(origin=DuplicateIdError(_id, self))
        self.data[_id] = value
