from abc import abstractmethod

import boto3
from botocore.exceptions import ClientError

from common.cloud_services import Service
from common.interfaces.repository import Repository
# from common.interfaces.logger import Logger
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
