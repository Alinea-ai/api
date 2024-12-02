from django.http import HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q

from alinea_api.models import CustomUser
from alinea_api.serializers import UserSerializer


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
        200: openapi.Response('List of users', UserSerializer(many=True)),
        400: 'Bad Request',
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
    phone_number = request.GET.get('phone', '').strip()

    if not name and not phone_number:
        return HttpResponseBadRequest('At least one search parameter (name or phone_number) is required.')

    # Initialize the queryset
    queryset = CustomUser.objects.all()

    # Apply filters based on provided parameters
    if name:
        # Filter on first_name, last_name, or username
        queryset = queryset.filter(
            Q(first_name__icontains=name) |
            Q(last_name__icontains=name) |
            Q(username__icontains=name)
        )
    if phone_number:
        # Assuming you have a Profile model related to User with a phone_number field
        queryset = queryset.filter(phone_number__icontains=phone_number)

    # Serialize the data
    serializer = UserSerializer(queryset, many=True)

    return Response(serializer.data)
