import base64
import binascii

import api.v1.function as lib

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from core.user.models import User, DWHUser
from library.constant.error_codes import (
    BASIC_AUTH_NOT_FOUND, BASIC_AUTH_NOT_VALID, BEARER_TOKEN_NOT_FOUND,
    BEARER_TOKEN_NOT_VALID, ERROR_CODE_MESSAGE, INVALID_LOGIN,
    INVALID_PASSWORD, INVALID_USERNAME
)
from library.functions import now


# check token authorize
class TokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_FOUND,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_FOUND]
            })

        if len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
            })

        receive_token = auth[1]

        user_id = self.parse_token(receive_token)
        if not user_id:
            raise exceptions.AuthenticationFailed({
                'error_code': BEARER_TOKEN_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
            })

        return self.check_user_and_token(user_id, request)

    @staticmethod
    def parse_token(key):
        try:
            receive_token = base64.b64decode(key)
            receive_token = receive_token.decode()

            # _info_list = receive_token.split(':')
            # if len(_info_list) != 2:
            #     return None, None

            user_id = receive_token
            # token = _info_list[1]

            return user_id
        except ValueError:
            return None

    def authenticate_header(self, request):
        return self.keyword

    @staticmethod
    def check_user_and_token(user_id, request=None):
        # try:
        #     user = User.objects.get(id=user_id)
        # except User.DoesNotExist:
        #     raise exceptions.AuthenticationFailed({
        #         'error_code': BEARER_TOKEN_NOT_VALID,
        #         'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
        #     })
        #
        # if token != user.token:
        #     raise exceptions.AuthenticationFailed({
        #         'error_code': BEARER_TOKEN_NOT_VALID,
        #         'description': ERROR_CODE_MESSAGE[BEARER_TOKEN_NOT_VALID]
        #     })

        con, cur = lib.connect()

        sql = """
             select obi.CRM_DWH_PKG.FUN_GET_LOGIN(P_USER_NAME=>'{}') FROM DUAL
                    """.format(user_id)
        cur.execute(sql)
        res = cur.fetchone()

        if res:
            data_cursor = res[0]

            for data in data_cursor:
                user = DWHUser(
                    username=data[0],
                    password=data[2],
                    fullname=data[1],
                    jobtitle=data[3],
                    avatar=data[4]
                )
            cur.close()
            con.close()

            setattr(request, 'user', user)

            return user, user.token
        else:
            cur.close()
            con.close()
            return None, None


class TokenAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'api.base.authentication.TokenAuthentication'
    name = 'TokenAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer"
        }


# Login authorize
class BasicAuthentication(BaseAuthentication):
    """
        HTTP Basic authentication against username/password.
        """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            raise exceptions.AuthenticationFailed({
                'error_code': BASIC_AUTH_NOT_FOUND,
                'description': ERROR_CODE_MESSAGE[BASIC_AUTH_NOT_FOUND]
            })

        if len(auth) == 1 or len(auth) > 2:
            raise exceptions.AuthenticationFailed({
                'error_code': BASIC_AUTH_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BASIC_AUTH_NOT_VALID]
            })

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
            username, password = auth_parts[0], auth_parts[2]
        except (TypeError, UnicodeDecodeError, binascii.Error):
            raise exceptions.AuthenticationFailed({
                'error_code': BASIC_AUTH_NOT_VALID,
                'description': ERROR_CODE_MESSAGE[BASIC_AUTH_NOT_VALID]
            })

        return self.check_username_password(username, password, request)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm

    @staticmethod
    def check_username_password(username, password, request=None):
        if not username or not password:
            raise exceptions.AuthenticationFailed({
                'error_code': INVALID_LOGIN,
                'description': ERROR_CODE_MESSAGE[INVALID_LOGIN]
            })

        # user = User.objects.filter(username=username).first()
        # if user is None:
        #     raise exceptions.AuthenticationFailed({
        #         'error_code': INVALID_USERNAME,
        #         'description': ERROR_CODE_MESSAGE[INVALID_USERNAME]
        #     })
        #
        # if not user.check_password(password):
        #     raise exceptions.AuthenticationFailed({
        #         'error_code': INVALID_PASSWORD,
        #         'description': ERROR_CODE_MESSAGE[INVALID_PASSWORD]
        #     })
        #
        # user.last_login = now()
        # user.save()
        user = User(
            id=0,
            name='test',
            token='abc'
        )
        setattr(request, 'user', user)

        return user, None  # authentication successful

