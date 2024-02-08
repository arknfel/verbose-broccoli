from common.root_aggregate import Actor


class ServiceConfigError(Actor.config_type.error_type): ...


class ServiceError(Actor.error_type): ...


class ServiceConfig(Actor.config_type):
    error_type = ServiceConfigError


class Service(Actor):
    error_type = ServiceError
    config_type = ServiceConfig
