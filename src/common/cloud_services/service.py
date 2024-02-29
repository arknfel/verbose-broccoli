from abc import abstractmethod

from common.root_aggregate import Actor


class ServiceConfig(Actor.config_type):
    @property
    @abstractmethod
    def provider(self): ...


class Service(Actor):
    config_type = ServiceConfig


# class ServiceActionConfig(Service.config_type): ...


# class ServiceAction(Service): ...
