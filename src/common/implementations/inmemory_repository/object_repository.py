from common.root_aggregate import UnexpectedError
from common.interfaces import Repository


class ObjectRepositoryError(Repository.error_type): ...


class ObjectRepository(Repository):
    error_type = ObjectRepositoryError

    def get(self, _id: str, default=None):
        return getattr(self.repo, _id, default)

    def put(self, _id: str, value):
        if not hasattr(self.repo, _id) or isinstance(getattr(type(self.repo), _id), property):
            raise self.error_type(f"'{_id}' is not a registered property")
        try:
            setattr(self.repo, _id, value)
        except AttributeError as e:
            raise self.error_type(origin=e)
        except Exception as e:
            raise self.error_type(origin=UnexpectedError(origin=e))
