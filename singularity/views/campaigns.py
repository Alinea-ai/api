from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def prospects(request):
    """
    Search for users by name and/or phone number.

    Query Parameters:
    - name: (optional) The name of the user to search for.
    - phone_number: (optional) The phone number of the user to search for.

    At least one query parameter must be provided.
    """

    return JsonResponse({"test": True})