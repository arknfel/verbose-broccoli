from common.services import Service


class AWSServiceConfigError(Service.config_type.error_type): ...


class AWSServiceError(Service.error_type): ...


class AWSServiceConfig(Service.config_type):
    error_type = AWSServiceConfigError

    @property
    def account_id(self):
        return self.repo.get('account_id')

    @property
    def region(self):
        return self.repo.get('region')


class AWSService(Service):
    error_type = AWSServiceError
    config_type = AWSServiceConfig
