from inspect import isclass

from common.interfaces import repository
from common.root_aggregate.error import UnexpectedError

from .entity import Entity
from .value_object import ValueObject


class Config(ValueObject): ...


class Actor(Entity):
    config: Config
    config_type = Config

    def __init__(self, configs: repository):
        if hasattr(self, '__annotations__'):
            for name, _type in self.__annotations__.items():
                try:
                    # breakpoint()
                    if isclass(_type) and issubclass(_type, ValueObject):
                        obj: ValueObject = _type(configs)
                    elif isclass(_type) and issubclass(_type, Actor):
                        obj: Actor = _type(self.config.value)
                    setattr(self, name, obj)
                    obj.owner = self
                except Entity.error as e:
                    raise self.error(origin=e)
                except Exception as e:
                    raise self.error(origin=UnexpectedError(origin=e))


class Action(Actor): ...
