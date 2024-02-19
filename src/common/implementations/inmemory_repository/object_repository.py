from common.root_aggregate.error import UnexpectedError
from common.interfaces import Repository


class ObjectRepositoryError(Repository.error): ...


class ObjectRepository(Repository):
    # error_type = ObjectRepositoryError
    data: 'ObjectRepository'

    def get(self, _id: str, default=None):
        return getattr(self.data, _id, default)

    def put(self, _id: str, value):
        if not hasattr(self.data, _id) or isinstance(getattr(type(self.data), _id), property):
            raise self.error(f"'{_id}' is not a registered property")
        try:
            setattr(self.data, _id, value)
        except AttributeError as e:
            raise self.error(origin=e)
        except Exception as e:
            raise self.error(origin=UnexpectedError(origin=e))
