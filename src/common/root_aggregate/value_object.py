from abc import abstractmethod
from inspect import isclass

from common.implementations.inmemory_repository import ObjectRepository


class ValueObject(ObjectRepository):
    types = set()
    default = None

    @property
    @abstractmethod
    def label(self): ...

    def __init__(self, data):
        super().__init__(data)

        self._value = self.data.get(self.label, self.default)
        self.validate()
        if hasattr(self, '__annotations__'):
            for name, _type in self.__annotations__.items():
                try:
                    if isclass(_type) and issubclass(_type, ValueObject):
                        value_object: ValueObject = _type(self._value)
                        setattr(self, name, value_object)
                        value_object.owner = self
                except _type.error as e:
                    raise self.error(origin=e)

    @property
    def value(self):
        return self._value

    def validate(self):
        if self.types and type(self._value) not in self.types:
            raise self.error(
                f"Invalid value type, got value '{self._value}' of type {type(self._value)}, allowed are: {self.types}"
            )
