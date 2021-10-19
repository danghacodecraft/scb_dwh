import datetime
import json

from django.core.paginator import EmptyPage, Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation
from loguru import logger
from rest_framework import exceptions, status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.base.authentication import TokenAuthentication
from api.base.exception import CustomAPIException
from api.base.schemas import \
    custom_open_api_type_datetime  # noqa: dùng để custom lại format datetime openapi
from api.base.serializers import EmptyRequestSerializer
from config.root_local import LOGGER_PRINT
from config.settings import DATETIME_INPUT_OUTPUT_FORMAT, DEFAULT_LANGUAGE_ID
from library.constant.api import (
    ORDER_BY_DESC, PAGINATOR_PER_PAGE, SORT_TYPE_TO_ID
)
from library.constant.error_codes import ERROR_CODE_MESSAGE
from library.constant.language import (
    ID_TO_LANGUAGES, LANGUAGE_TYPE_VIETNAMESE, LANGUAGES_TO_ID
)
from library.functions import datetime_to_string


class DjangoOverRideJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = datetime_to_string(o, DATETIME_INPUT_OUTPUT_FORMAT)
            return r
        else:
            return super(DjangoOverRideJSONEncoder, self).default(o)


class CustomAPIView(GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    parser_classes = (JSONParser,)
    serializer_class = EmptyRequestSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.called_from_c_system_type = None
        self.is_paging = False
        self.total_page = None
        self.total_record = None
        self.per_page = PAGINATOR_PER_PAGE
        self.page = 1
        self.paging_list = None
        self.current_page = None
        self.sort = ORDER_BY_DESC  # default sort via children by desc
        self.lang = DEFAULT_LANGUAGE_ID
        self.lang_code = ID_TO_LANGUAGES[DEFAULT_LANGUAGE_ID]
        self.order_by = 'id'

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)

        if LOGGER_PRINT:
            # logger.info(response.data)

            from django.db import connection
            for query in connection.queries:
                logger.debug(f"\n{query['sql']}")
                logger.debug(f"\n{query['time']}")

            logger.info(f"Total number of queries = {len(connection.queries)}")
            logger.success("Query Complete!")

        return response

    def initial(self, request, *args, **kwargs):
        self.renderer_classes = (JSONRenderer,)

        self.parse_common_params(request)
        translation.activate(self.lang_code)

    def parse_common_params(self, request):
        self.lang_code = request.META.get('HTTP_MNV_LANGUAGE', ID_TO_LANGUAGES.get(LANGUAGE_TYPE_VIETNAMESE))
        self.lang = LANGUAGES_TO_ID.get(self.lang_code, LANGUAGE_TYPE_VIETNAMESE)
        self.sort = SORT_TYPE_TO_ID.get(request.GET.get('sort', 'desc'), ORDER_BY_DESC)

        per_page = self.request.query_params.get('limit', None)
        if per_page and per_page.isdigit():
            self.per_page = int(per_page)

        page = self.request.query_params.get('page', None)
        if page and page.isdigit():
            self.page = int(page)

    def paginate(self, query_set):
        is_order = getattr(query_set, 'ordered', None)
        if not is_order:
            query_set = query_set.order_by(self.order_by)

        paginator = Paginator(query_set, per_page=self.per_page)

        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except EmptyPage:
            self.paging_list = []

    @staticmethod
    def _response(data, status_code=status.HTTP_200_OK):
        return Response(json.loads(json.dumps(data, cls=DjangoOverRideJSONEncoder)), status=status_code)

    def response_paging(self, data):
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        return self._response({
            'items': data,
            'total_page': self.total_page,
            'total_record': len(data) if not self.is_paging and isinstance(data, list) else self.total_record,
            'page': self.page,
        })

    def response_success(self, data, status_code=status.HTTP_200_OK):
        return self._response(data, status_code)

    def http_exception(self, error_code=None, description=None, status_code=status.HTTP_400_BAD_REQUEST):
        raise CustomAPIException(status_code=status_code, detail={
            'error_code': error_code,
            'description': ERROR_CODE_MESSAGE.get(error_code, '') if not description else description
        })

    def check_key_content(self, key_content_list, check_key_list):
        list_key_missing = list()
        for key in check_key_list:
            if key not in key_content_list:
                list_key_missing.append(key)
        if len(list_key_missing) > 0:
            return self.http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Missing ' + ", ".join(list_key_missing)
            )

    def get_model_object_by_id(self, id: int, model, message: str = None):  # noqa
        try:
            obj = model.objects.get(id=id)
        except model.DoesNotExist as ex:
            if message is None:
                message = str(ex)
            return self.http_exception(description=message)
        return obj
