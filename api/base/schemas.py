from drf_spectacular.types import OPENAPI_TYPE_MAPPING, OpenApiTypes

from library.functions import datetime_to_string, now


# Mặc định field nào datetime thì openapi sẽ tự tạo example là: 2019-08-24T14:15:22Z
# custom lại theo format DATETIME_INPUT_OUTPUT_FORMAT
def custom_open_api_type_datetime():
    OPENAPI_TYPE_MAPPING[OpenApiTypes.DATETIME].update({'example': datetime_to_string(now())})


custom_open_api_type_datetime()
