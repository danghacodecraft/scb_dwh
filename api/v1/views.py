from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view


from library.otp import get_otp


@api_view(['GET'])
def get_otp_server(request):
    if request.method == 'GET':
        _otp = get_otp(10)

        status_code = status.HTTP_200_OK

        return Response({'otp': _otp[1]}, status=status_code)
