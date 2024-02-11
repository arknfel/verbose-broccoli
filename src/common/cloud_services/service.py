from abc import abstractmethod

from common.root_aggregate import Actor


class ServiceConfigError(Actor.config_type.error_type): ...


class ServiceError(Actor.error_type): ...


class ServiceConfig(Actor.config_type):
    error_type = ServiceConfigError

    @abstractmethod
    def provider(self): ...


class Service(Actor):
    error_type = ServiceError
    config_type = ServiceConfig


class ServiceActionConfigError(Service.config_type.error_type): ...


class ServiceActionError(Service.error_type): ...


class ServiceActionConfig(Service.config_type):
    error_type = ServiceActionConfigError


class ServiceAction(Service):
    error_type = ServiceActionError
    config_type = ServiceActionConfig