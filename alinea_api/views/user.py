from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from alinea_api.models import UserPersonalInformation
from alinea_api.serializers import UserPersonalInformationSerializer


@swagger_auto_schema(
    method='get',
    operation_description="Search users by name and/or phone number",
    manual_parameters=[
        openapi.Parameter(
            'name',
            openapi.IN_QUERY,
            description="Name of the user to search for (partial matches allowed)",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'phone_number',
            openapi.IN_QUERY,
            description="Phone number of the user to search for (partial matches allowed)",
            type=openapi.TYPE_STRING
        ),
    ],
    responses={
        400: 'Bad Request'
    }
)
@api_view(['GET'])
def search_users(request):
    """
    Search for users by name and/or phone number.

    Query Parameters:
    - name: (optional) The name of the user to search for.
    - phone_number: (optional) The phone number of the user to search for.

    At least one query parameter must be provided.
    """
    name = request.GET.get('name', '').strip()
    phone_number = request.GET.get('phone_number', '').strip()

    if not name and not phone_number:
        return HttpResponseBadRequest('At least one search parameter (name or phone_number) is required.')

    # Initialize the queryset
    queryset = UserPersonalInformation.objects.all()

    # Apply filters based on provided parameters
    if name:
        queryset = queryset.filter(name__icontains=name)
    if phone_number:
        queryset = queryset.filter(phone__icontains=phone_number)

    # Serialize the data
    serializer = UserPersonalInformationSerializer(queryset, many=True)

    return Response(serializer.data)