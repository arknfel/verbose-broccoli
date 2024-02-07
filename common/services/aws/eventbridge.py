from common.services.aws import AWSService


class AWSEventbridgeConfigError(AWSService.config_type.error_type): ...


class AWSEventbridgeError(AWSService.error_type): ...


class AWSEventbridgeConfig(AWSService.config_type):
    error_type = AWSEventbridgeConfigError


class AWSEventbridge(AWSService):
    error_type = AWSEventbridgeError
