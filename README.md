<!-- PROJECT LOGO -->
<div align="center"><br />
<p align="center" style="width: 100%">
    <img src="https://minerva.vn/wp-content/uploads/2020/06/logo.png" alt="Logo" style="-webkit-user-select: none;margin: auto;">

<h3 align="center">DWH</h3>
</p>
</div>


DWH for SCB platform. Base from Django + Oracle

## I. Requirements:
    - python >= 3.8.10

## II. Setup environment:
- How to set up environment:
    1. Install [cx_oracle](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html)
    2. Setup Python virtual environment:

        For Linux:
        ```sh
        cd base-django
        virtualenv env -p python3
        source env/bin/activate
        pip install -r requirements.txt
        ```

        For Windows:
        ```powershell
        cd base-django
        virtualenv env -p py3
        env/Scripts/activate
        pip install -r requirements_windows.txt
        ```

        Lưu ý: một số package trên linux và windows khác nhau nên chú ý file requirements tương ứng OS.
    3. Install ``pre-commit``: `pre-commit install`
    4. In folder `config`
        - Copy a content of file `database.py.yml` to `database.py` file and config some parameters in it if necessary (`already configured`).
        - Copy a content of file `root_local.py.yml` to `root_local.py` file and config some parameters in it if necessary (`already configured`).
            **NOTE**:
            - CHANGE `LOCAL_SECRET_KEY` FOR PRODUCTION. This key should be unique and kept private for each server. To generate a new key for each deployment, `cd` to the main source code directory (the one contains the `manage.py` file) and run the following command:
                ```shell
                $ python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
                ```
            - CHANGE `LOCAL_DEBUG=False` FOR PRODUCTION: This should be set to `False`.

    5. Run
        - For local development: type command `python manage.py runserver <host>:<port>`
            ```sh
            python manage.py runserver 127.0.0.1:8000
            ```
        - For production: Use [`Gunicorn`](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/gunicorn/) to start server.

    6. Documentation
        - Swagger: `http://127.0.0.1:8000/api/v1/docs/`
        - Redoc: `http://127.0.0.1:8000/api/v1/redoc/`


## III. Note for developers:
- Cách lấy bearer token để dùng cho các api trong BaseAPIView:
    -  Gọi api `/api/v1/users/login/` dùng Basic Auth
        -  username mặc định:  `admin`
    	-  password mặc định:  `123`
    -  Hoặc chạy đoạn cUrl sau:
        ```curl
        curl --location --request POST 'http://127.0.0.1:8000/api/v1/users/login/' --header 'Authorization: Basic YWRtaW46MTIz'
        ```
