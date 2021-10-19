from django.utils.translation import ugettext_lazy as _

# API error code & messages
JSON_BODY_EMPTY = 'JSON_BODY_EMPTY'
BODY_PARSE_ERROR = 'JSON_BODY_EMPTY'
BASIC_AUTH_NOT_FOUND = 'BASIC_AUTH_NOT_FOUND'
BASIC_AUTH_NOT_VALID = 'BASIC_AUTH_NOT_VALID'
BEARER_TOKEN_NOT_FOUND = 'BEARER_TOKEN_NOT_FOUND'
BEARER_TOKEN_NOT_VALID = 'BEARER_TOKEN_NOT_VALID'

INVALID_LOGIN = 'INVALID_LOGIN'
INVALID_USERNAME = 'INVALID_USERNAME'
INVALID_PASSWORD = 'INVALID_PASSWORD'

# user
ERROR_USERNAME_IS_EXISTED = 'ERROR_USERNAME_IS_EXISTED'

ERROR_CODE_MESSAGE = {
    JSON_BODY_EMPTY: _('Json body empty'),
    BODY_PARSE_ERROR: _('Parsing body occurred error'),
    BASIC_AUTH_NOT_FOUND: _('Can not found basic auth in header'),
    BASIC_AUTH_NOT_VALID: _('Basic auth is not valid'),
    BEARER_TOKEN_NOT_FOUND: _('Can not found bearer token in header'),
    BEARER_TOKEN_NOT_VALID: _('Bearer token is not valid'),

    INVALID_LOGIN: _('INVALID_LOGIN'),
    INVALID_USERNAME: _('INVALID_USERNAME'),
    INVALID_PASSWORD: _('INVALID_PASSWORD'),

    ERROR_USERNAME_IS_EXISTED: _('username is existed')

}
