import base64
import binascii

import cx_Oracle
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework import status, exceptions, HTTP_HEADER_ENCODING
import ldap
from rest_framework.authentication import get_authorization_header

import api.v1.function as lib

from api.base.authentication import BasicAuthentication
from api.base.base_views import BaseAPIView
from api.base.serializers import ExceptionResponseSerializer
from api.v1.user.schemas import (
    EXAMPLE_RESPONSE_LIST_PAGING_USERS_SUCCESS,
    EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_LOGIN,
    EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_PASSWORD,
    EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_USERNAME,
    EXAMPLE_RESPONSE_LOGIN_SUCCESS1, EXAMPLE_RESPONSE_LOGIN_SUCCESS2
)
from api.v1.user.serializers import (
    UserCreateRequestSerializer, UserCreateSuccessResponseSerializer,
    UserDetailSuccessResponseSerializer,
    UserListPagingSuccessResponseSerializer, UserListSuccessResponseSerializer,
    UserLoginSuccessResponseSerializer, UserUpdateRequestSerializer
)
from core.user.models import User, DWHUser
from library.constant.error_codes import ERROR_USERNAME_IS_EXIST

from config.settings import LDAP_SERVER, LDAP_DOMAIN


class UserView(BaseAPIView):
    @extend_schema(
        operation_id='user-create',
        summary='Create',
        tags=["User"],
        description='Create new user',
        request=UserCreateRequestSerializer,
        responses={
            status.HTTP_201_CREATED: UserCreateSuccessResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def create(self, request):
        serializer = UserCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']
        username = serializer.validated_data['username'].lower()
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return self.http_exception(error_code=ERROR_USERNAME_IS_EXIST)

        user = User.objects.create(
            name=name,
            username=username
        )
        user.set_password(password)
        user.save()

        return self.response_success({
            'user_id': user.id,
            'name': user.name
        }, status_code=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id='user-detail',
        summary='Detail',
        tags=["User"],
        description='Detail an user',
        responses={
            status.HTTP_200_OK: UserDetailSuccessResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def read(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist as ex:
            return self.http_exception(description=str(ex))

        return self.response_success({
            'id': user.id,
            'name': user.name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        })

    @extend_schema(
        operation_id='user-update',
        summary='Update',
        tags=["User"],
        description='Update an user',
        request=UserUpdateRequestSerializer,
        responses={
            status.HTTP_200_OK: UserDetailSuccessResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def update(self, request, user_id):
        serializer = UserUpdateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data['name']

        user = self.get_model_object_by_id(user_id, User)

        user.name = name
        user.save()

        return self.response_success({
            'id': user.id,
            'name': user.name,
            'created_at': user.created_at,
            'updated_at': user.updated_at
        })

    @extend_schema(
        operation_id='user-delete',
        summary='Delete',
        tags=["User"],
        description='Delete an user',
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        }
    )
    def delete(self, request, user_id):
        user = self.get_model_object_by_id(user_id, User)
        user.delete()

        return self.response_success(None, status_code=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        operation_id="list-all-users-paging",
        summary="List",
        tags=["User"],
        description="List all users paging in system",
        responses={
            status.HTTP_200_OK: UserListPagingSuccessResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
            status.HTTP_400_BAD_REQUEST: ExceptionResponseSerializer,
        },
        examples=[EXAMPLE_RESPONSE_LIST_PAGING_USERS_SUCCESS],
    )
    def list(self, request):
        """
        [API] Get all users in system
        """
        users = User.objects.all().values("name", "username", "id")
        self.paginate(users)

        response = UserListSuccessResponseSerializer(self.paging_list, many=True)

        return self.response_paging(response.data)

    def get(self, request):
        user = request.user

        return self.response_success({
            'user_id': user.id,
            'full_name': user.name,
            'token': user.token,
            'avatar': user.avatar,
            'position': user.position,
            'department': user.department,
            'jobtitle': user.jobtitle,
            'branch_code': user.branch_code,
            'employee_id': user.employee_id,
            'email': user.email
        }, status_code=status.HTTP_200_OK)


# Login hông dùng Bearer token mà dùng Basic authentication (truyền username, password)
# nên sửa riêng authentication_classes
class LoginView(BaseAPIView):
    # setting user/password authentication.
    # Bypass authentication_classes
    authentication_classes = (BasicAuthentication,)

    @extend_schema(
        operation_id='user-login',
        summary='Login',
        tags=["User"],
        description='Login to get Bearer token to use in others API',
        # parameters=[
        #     OpenApiParameter(
        #         name="username", type=OpenApiTypes.STR, description="1. Tài khoản"
        #     ),
        #     OpenApiParameter(
        #         name="password", type=OpenApiTypes.STR, description="2. Mật khẩu"
        #     )
        # ],
        responses={
            status.HTTP_200_OK: UserLoginSuccessResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: ExceptionResponseSerializer,
        },
        examples=[
            EXAMPLE_RESPONSE_LOGIN_SUCCESS1,
            EXAMPLE_RESPONSE_LOGIN_SUCCESS2,
            EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_LOGIN,
            EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_USERNAME,
            EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_PASSWORD
        ]
    )
    def login(self, request):
        if request.user:
            return self.response_success({
                'user_id': request.user.id,
                'full_name': request.user.name,
                'token': request.user.token,
                'avatar': request.user.avatar,
                'position': request.user.position,
                'department': request.user.department,
                'jobtitle': request.user.jobtitle,
                'branch_code': request.user.branch_code,
                'employee_id': request.user.employee_id,
                'email': request.user.email
            }, status_code=status.HTTP_200_OK)
        else:
            return self.response_success({"error": "Sai thông tin"},
                                         status_code=status.HTTP_401_UNAUTHORIZED)
