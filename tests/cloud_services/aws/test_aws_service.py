from unittest import TestCase

from common.cloud_services.aws.service import AWSService, AWSServiceConfig
from common.implementations.inmemory_repository import DictRepository


class TestAWSService(TestCase):

    def test_init(self):
        class S3ServiceConfig(AWSServiceConfig):
            @property
            def label(self):
                return self.service_name

            @property
            def service_name(self):
                return 's3'

        class S3Service(AWSService):
            config: S3ServiceConfig

        config_meta = {
            's3': {
                'account_id': 123,
                'region_name': 'eu-central-1'
            }
        }
        repo = DictRepository(config_meta)
        svc = S3Service(repo)
        assert svc
