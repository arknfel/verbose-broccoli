from ... import AWSService
from ....interfaces import Events
from .actions import PutRule


class AWSEventsConfigError(AWSService.config_type.error_type): ...


class AWSEventsError(AWSService.error_type): ...


class AWSEventsConfig(AWSService.config_type):
    error_type = AWSEventsConfigError

    @property
    def service_name(self):
        return 'events'


class AWSEvents(AWSService, Events):
    error_type = AWSEventsError
    config_type = AWSEventsConfig

    def put_rule(self):
        return PutRule(self, self.config)
