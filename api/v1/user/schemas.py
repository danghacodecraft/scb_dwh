from drf_spectacular.utils import OpenApiExample

EXAMPLE_RESPONSE_LOGIN_SUCCESS1 = OpenApiExample(
    name='Login success 1',
    summary='1',
    description='''
    Tài khoản mặc định:
        username: THANGHD
        password: THANGHD@321
    Lưu ý: Gửi basic auth trên header, không phải gửi qua payload body
    ''',
    value={
        'user_id': 'THANGHD',
        'name': 'Hồ Đức Thắng',
        'token': 'VEhBTkdIRA==',
    },
    status_codes=["200"],
    # request_only=True,  # signal that example only applies to requests
    response_only=True  # signal that example only applies to responses
)

EXAMPLE_RESPONSE_LOGIN_SUCCESS2 = OpenApiExample(
    name='Login success 2',
    summary='2',
    description='This is an example response when when login success',
    value={
        'user_id': '456',
        'name': 'Test 2',
        'token': 'MjY0OjQyYzE4NTVhZmUwY2ZkMDY2MTJmMzY2N2ViODA5OTYzZTliMGMxOGQ=',
    },
    status_codes=["200"],
    # request_only=True,  # signal that example only applies to requests
    response_only=True  # signal that example only applies to responses
)

EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_LOGIN = OpenApiExample(
    name='Login fail 1',
    summary='Empty username or password',
    description='username or password is empty',
    value={
        'error_code': 'INVALID_LOGIN',
        'description': 'INVALID_LOGIN'
    },
    status_codes=["401"],
    response_only=True
)

EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_USERNAME = OpenApiExample(
    name='Login fail 2',
    summary='Invalid username',
    description='username is not exist',
    value={
        'error_code': 'INVALID_USERNAME',
        'description': 'INVALID_USERNAME'
    },
    status_codes=["401"],
    response_only=True
)

EXAMPLE_RESPONSE_LOGIN_FAIL_INVALID_PASSWORD = OpenApiExample(
    name='Login fail 3',
    summary='Invalid password',
    description='password is not valid',
    value={
        'error_code': 'INVALID_PASSWORD',
        'description': 'INVALID_PASSWORD'
    },
    status_codes=["401"],
    response_only=True
)

EXAMPLE_RESPONSE_LIST_PAGING_USERS_SUCCESS = OpenApiExample(
    name="List success",
    summary="1",
    description="List all users",
    value={
        "items": [
            {
                "name": "ADMIN",
                "username": "admin",
                "id": 21
            }
        ],
        "total_page": 1,
        "total_record": 1,
        "page": 1
    },
    response_only=True,
)
