from abc import abstractmethod

import boto3
from botocore.config import Config

from common.cloud_services import Service
from common.interfaces.repository import Repository
from common.interfaces.logger import Logger


class AWSServiceConfigError(Service.config_type.error_type): ...


class AWSServiceError(Service.error_type): ...


class AWSServiceConfig(Service.config_type):
    error_type = AWSServiceConfigError

    @abstractmethod
    @property
    def service_name(self): ...

    @property
    def provider(self):
        return 'AWS'

    @property
    def account_id(self):
        return self.repo.get('account_id')

    @property
    def region(self):
        return self.repo.get('region')

    @property
    def kwargs(self):
        return {'service_name': self.service_name, **self.repo.get('kwargs', {})}

    @property
    def client_config(self):
        return Config(self.repo.get('client_config', {}))


class AWSService(Service):
    error_type = AWSServiceError
    config_type = AWSServiceConfig

    def __init__(self, repo: Repository, *args, **kwargs):
        super().__init__(repo, *args, **kwargs)
        self.config: AWSServiceConfig

        self.client = boto3.client(**kwargs, config=self.config.client_config)


class AWSActionConfigError(AWSService.config_type.error_type): ...


class AWSActionError(AWSService.error_type): ...


class AWSActionConfig(AWSService.config_type):
    error_type = AWSActionConfigError

    @abstractmethod
    def action_name(self): ...


class AWSAction(AWSService.action):
    error_type = AWSActionError
    config_type = AWSActionConfig

    def __init__(self, service: AWSService, repo: Repository, *args, **kwargs):
        self.service = service