from rest_framework import HTTP_HEADER_ENCODING, exceptions

from api.base.api_view import CustomAPIView
from config.root_local import SERVER_AUTH_TOKEN
from library.constant.error_codes import SERVER_AUTH_NOT_FOUND


class BaseAPIView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        self.user = request.user

        # Đối với ServerAuthentication thì gán thêm called_from_c_system_type để biết call từ bên nào
        self.called_from_c_system_type = request.auth


class BaseAPIAnonymousView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # có bearer token trong header thì check token mới hoạt động
        if self.get_authorization_header(request).split():
            self.user = request.user

    @staticmethod
    def get_authorization_header(request):
        server_auth = request.META.get('HTTP_SERVER_AUTH')
        if not (server_auth and server_auth == SERVER_AUTH_TOKEN):
            raise exceptions.AuthenticationFailed({
                'error_code': SERVER_AUTH_NOT_FOUND,
                'description': SERVER_AUTH_NOT_FOUND
            })

        content = request.META.get('HTTP_AUTHORIZATION', b'')
        try:
            content = content.encode(HTTP_HEADER_ENCODING)
        except Exception:  # noqa
            content = b''
        return content
