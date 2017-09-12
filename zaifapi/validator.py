import cerberus
import json
from decimal import Decimal
from zaifapi.api_error import ZaifApiValidationError


class ZaifApiValidator:
    def __init__(self):
        self._schema = _ZaifValidationSchema()

    def params_pre_processing(self, keys, params):
        self._validate(keys, params)
        return self._edit_params(params)

    @classmethod
    def _edit_params(cls, params):
        if 'from_num' in params:
            params['from'] = params['from_num']
            del (params['from_num'])
        return params

    def _validate(self, keys, params):
        required_schema = self._schema.select(keys)
        v = _UnitValidator(required_schema)
        if v.validate(params):
            return
        raise ZaifApiValidationError(json.dumps(v.errors))


class _UnitValidator(cerberus.Validator):
    @staticmethod
    def _validate_type_decimal(value):
        if isinstance(value, Decimal):
            return True

    def validate(self, params):
        return super().validate(params)


class _ZaifValidationSchema:
    def __init__(self):
        self._schema = DEFAULT_SCHEMA

    def all(self):
        return self._schema

    def select(self, keys):
        return dict(filter(lambda item: item[0] in keys, self._schema.items()))

    def update(self, key, value):
        pass


DEFAULT_SCHEMA = {
    'from_num': {
        'type': 'integer'
    },
    'count': {
        'type': 'integer'
    },
    'from_id': {
        'type': 'integer'
    },
    'end_id': {
        'type': ['string', 'integer']
    },
    'order': {
        'type': 'string',
        'allowed': ['ASC', 'DESC']
    },
    'since': {
        'type': 'integer'
    },
    'end': {
        'type': ['string', 'integer']
    },
    'currency_pair': {
        'type': 'string'
    },
    'currency': {
        'required': True,
        'type': 'string'
    },
    'address': {
        'required': True,
        'type': 'string'
    },
    'message': {
        'type': 'string'
    },
    'amount': {
        'required': True,
        'type': ['number', 'decimal']
    },
    'opt_fee': {
        'type': 'number'
    },
    'order_id': {
        'required': True,
        'type': 'integer'
    },
    'action': {
        'required': True,
        'type': 'string',
        'allowed': ['bid', 'ask']
    },
    'price': {
        'required': True,
        'type': ['number', 'decimal']
    },
    'limit': {
        'type': ['number', 'decimal']
    },
    'is_token': {
        'type': 'boolean'
    },
    'is_token_both': {
        'type': 'boolean'
    },
    'comment': {
        'type': 'string'
    },
    'group_id': {
        'type': ['string', 'integer']
    }
}
