from abc import abstractmethod

import boto3
from botocore.exceptions import ClientError

from common.cloud_services import Service
from common.interfaces.repository import Repository
from common.interfaces.logger import Logger
from common.root_aggregate.error import UnexpectedError
from .properties import AwsAccountId, AwsRegion, AwsClientKwargs, AwsClientConfig


class AWSServiceConfig(Service.config_type):
    @property
    @abstractmethod
    def service_name(self): ...

    @property
    def provider(self):
        return 'AWS'

    account_id: AwsAccountId
    region: AwsRegion
    kwargs: AwsClientKwargs
    client_config: AwsClientConfig

    # @property
    # def account_id(self):
    #     return self.data.get('account_id')

    # @property
    # def region(self):
    #     return self.data.get('region')

    # @property
    # def kwargs(self):
    #     kwargs: dict = self.data.get('kwargs', {})
    #     kwargs.update({'service_name': self.service_name})
    #     return kwargs

    # @property
    # def client_config(self):
    #     client_config = self.data.get('client_config')
    #     if client_config:
    #         return Config(client_config)
    #     return None


class AWSService(Service):
    config: AWSServiceConfig

    def __init__(self, configs: Repository):
        super().__init__(configs)
        try:
            self.config.kwargs.value.update({
                'service_name': self.config.service_name,
                'region_name': self.config.region.value,
            })
            self.client = boto3.client(**self.config.kwargs.value, config=self.config.client_config.value)
        except ClientError as e:
            raise self.error(origin=e)
        except Exception as e:
            raise self.error(origin=UnexpectedError(origin=e))


# class AWSActionConfig(AWSService.config_type):
#     @abstractmethod
#     def action_name(self): ...


# class AWSAction(AWSService.action):
#     config_type = AWSActionConfig
