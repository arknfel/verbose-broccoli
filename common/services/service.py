from common.root_aggregate import Actor, Config
from common.root_aggregate.error import ActorError, ConfigError


class ServiceConfigError(ConfigError): ...


class ServiceError(ActorError): ...


class ServiceConfig(Config):
    error_type = ServiceConfigError


class Service(Actor):
    error_type = ServiceError
