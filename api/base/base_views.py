from rest_framework import HTTP_HEADER_ENCODING

from api.base.api_view import CustomAPIView


class BaseAPIView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # self.user = request.user

        # # Đối với ServerAuthentication thì gán thêm called_from_c_system_type để biết call từ bên nào
        # self.called_from_c_system_type = request.auth


class BaseAPIAnonymousView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # có bearer token trong header thì check token mới hoạt động
        if self.get_authorization_header(request).split():
            self.user = request.user

    @staticmethod
    def get_authorization_header(request):
        content = request.META.get('HTTP_AUTHORIZATION', b'')
        try:
            content = content.encode(HTTP_HEADER_ENCODING)
        except Exception:  # noqa
            content = b''
        return content
