from abc import ABC, ABCMeta
from typing import Type

from .error import Error


class RootBaseDescriptor:
    def __get__(self, _, cls) -> Type['Root']:
        return cls


class Root(ABC):
    error = _error = Error
    _base = RootBaseDescriptor()


class EntityBaseDescriptor:
    def __get__(self, _, cls: Type[Root]) -> Type['Root']:
        return cls.__base__


class MetaEntity(ABCMeta):
    @property
    def error(cls: Type['Entity']):
        if cls._error is cls._base._error:
            if cls._base._error is cls._base._base._error:
                cls._base._error = cls._base.error
            cls._error = type(f'{cls.__name__}Error', (cls._base._error,), {})
        return cls._error


class Entity(Root, metaclass=MetaEntity):
    _base = EntityBaseDescriptor()
    _owner = Root()

    @property
    def error(self):
        return type(self).error

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, obj: 'Entity'):
        self._owner = obj
