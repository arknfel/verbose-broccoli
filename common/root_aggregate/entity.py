from abc import ABC

from .error import Error


class EntityError(Error): ...


class Entity(ABC):
    error_type = EntityError
