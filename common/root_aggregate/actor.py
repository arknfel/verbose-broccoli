from .entity import Entity
from common.interfaces import Repository


class ConfigError(Repository.error_type): ...


class Config(Entity):
    error_type = ConfigError

    def __init__(self, repo: Repository, *args, **kwargs):
        self.repo = repo
        self.validate(*args, **kwargs)

    def validate(self, *args, **kwargs):
        pass


class ActorError(Entity.error_type): ...


class Actor(Entity):
    error_type = ActorError
    config_type = Config

    def __init__(self, repo: Repository, *args, **kwargs):
        try:
            self.config = self.config_type(repo, *args, **kwargs)
        except self.config.error_type as e:
            raise self.error_type(origin=e)
