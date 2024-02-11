from abc import abstractmethod

from .entity import Entity
from common.interfaces import Repository
from common.implementations.inmemory_repository import ObjectRepository


class ConfigError(ObjectRepository.error_type): ...


class Config(ObjectRepository):
    error_type = ConfigError

    def __init__(self, repo: Repository, *args, **kwargs):
        super().__init__(repo)
        # self.repo = self.data
        self.validate(*args, **kwargs)

    def validate(self, *args, **kwargs):
        pass


class ActorError(Entity.error_type): ...


class Actor(Entity):
    error_type = ActorError
    config_type = Config

    def __init__(self, repo: Repository):
        try:
            self.config = self.config_type(repo)
        except self.config_type.error_type as e:
            raise self.error_type(origin=e)

    @property
    def action(self):
        return Action


class ActionConfigError(Config.error_type): ...


class ActionError(Actor.error_type): ...


class ActionConfig(Config):
    error_type = ActionConfigError

    @property
    @abstractmethod
    def action_name(self): ...


class Action(Actor):
    error_type = ActionError
    config_type = ActionConfig

    @abstractmethod
    def do(self): ...

    @abstractmethod
    def undo(self): ...
