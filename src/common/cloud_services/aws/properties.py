from types import NoneType
from botocore.config import Config

from common.root_aggregate.value_object import ValueObject


class AwsAccountId(ValueObject):
    label = 'account_id'
    types = {str, int}

    def validate(self):
        super().validate()

        if type(self.value) is str:
            self.value: str
            if not self.value.isalnum():
                raise self.error(f"invalid value for an {self.label}")


class AwsRegion(ValueObject):
    label = 'region_name'
    types = {str}


class AwsClientKwargs(ValueObject):
    label = 'kwargs'
    types = {NoneType, dict}
    default = {}
    value: dict


class AwsClientConfig(ValueObject):
    label = 'config'
    types = {NoneType, dict}

    @property
    def value(self):
        if not self._value:
            return None
        return Config(self._value)
