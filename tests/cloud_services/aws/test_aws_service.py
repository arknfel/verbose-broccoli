from unittest import TestCase

from common.cloud_services.aws.service import AWSService, AWSServiceConfig


class TestAWSService(TestCase):

    def test_init(self):
        class MockAWSServiceConfig(AWSServiceConfig):
            @property
            def label(self):
                return self.service_name

            @property
            def service_name(self):
                return 'mock_service'

        class MockAWSService(AWSService):
            config: MockAWSServiceConfig

        config_meta = {
            'mock_service': {
                'account_id': 123,
                'region': 'eu-central-1'
            }
        }
        svc = MockAWSService(config_meta)
