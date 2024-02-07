from abc import ABC

from common.implementations.memory_repository import DictRepository
from .error import EntityError, ConfigError, ActorError


class Entity(ABC):
    error_type = EntityError


class Config(DictRepository):
    error_type = ConfigError

    def __init__(self, event: dict, *args, **kwargs):
        super().__init__(event)
        self.validate(*args, **kwargs)

    def validate(self):
        pass


class Actor(Entity):
    error_type = ActorError
    config_type = Config

    def __init__(self, config):
        try:
            self.config = self.config_type(config)
        except self.config.error_type as e:
            raise self.error_type(origin=e)
