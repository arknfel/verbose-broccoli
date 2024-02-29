from ... import AWSService
from ....interfaces import Events
from .actions import PutRule


class AWSEventsConfig(AWSService.config_type):
    @property
    def service_name(self):
        return 'events'


class AWSEvents(AWSService, Events):
    config: AWSEventsConfig

    def put_rule(self):
        return PutRule(self, self.config)
