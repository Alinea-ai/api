from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view

from singularity.agents.sql_agent import SqlAgent
from singularity.services.users import UserService

sql_agent = SqlAgent()
user_service = UserService()

@api_view(['GET'])
def user_query(request):
    """
    Search for users by name and/or phone number.

    Query Parameters:
    - name: (optional) The name of the user to search for.
    - phone_number: (optional) The phone number of the user to search for.

    At least one query parameter must be provided.
    """
    query = request.GET.get('query', '').strip()
    user_id = request.GET.get('user_id', '').strip()

    if not query or not user_id:
        return HttpResponseBadRequest(
            'At least one search parameter (name or phone_number) is required.')
    prompt = f"the nex query must be based only for user {user_id} and not other user. Query: {query}"
    response = sql_agent.invoke(prompt)
    return JsonResponse({"response": response[0], "sql_query": response[1]})

@api_view(['GET'])
def user_summary(request):
    """
    Search for users by name and/or phone number.

    Query Parameters:
    - name: (optional) The name of the user to search for.
    - phone_number: (optional) The phone number of the user to search for.

    At least one query parameter must be provided.
    """
    request_id = request.GET.get('request_id', '').strip()
    if not request_id:
        return HttpResponseBadRequest(
            'At least one search parameter (name or phone_number) is required.')
    summary = user_service.get_documents_summary(request_id)
    return JsonResponse({"response": summary})