# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializer import (
    UserQuerySerializer,
    UserQueryResponseSerializer,
    UserSummarySerializer,
    UserSummaryResponseSerializer,
)
from singularity.agents.sql_agent import SqlAgent
from singularity.services.users import UserService

import logging

logger = logging.getLogger(__name__)

sql_agent = SqlAgent()
user_service = UserService()


class UserQueryView(APIView):
    """
    Handle user queries based on a search term and user ID.
    """
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Search for users based on query and user ID",
        operation_description="Search for users by providing a search query and specifying the user ID to base the query on.",
        manual_parameters=[
            openapi.Parameter(
                "query",
                openapi.IN_QUERY,
                description="The search query for the user.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="The ID of the user to base the query on.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: UserQueryResponseSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """
        Handle GET requests for user queries.
        """
        serializer = UserQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            logger.warning(f"UserQueryView: Invalid parameters - {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data['query']
        user_id = serializer.validated_data['user_id']

        prompt = f"the next query must be based only for user {user_id} and not other users. Query: {query}"
        try:
            response = sql_agent.invoke(prompt)
            if not isinstance(response, (list, tuple)) or len(response) < 2:
                logger.error(
                    f"UserQueryView: Unexpected response format from SQL agent - {response}")
                return Response(
                    {"error": "Unexpected response format from SQL agent."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            response_data = {
                "response": response[0],
                "sql_query": response[1]
            }
            response_serializer = UserQueryResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"UserQueryView: Exception occurred - {str(e)}")
            return Response(
                {"error": f"An error occurred while processing the query: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserSummaryView(APIView):
    """
    Handle user summaries based on a request ID.
    """
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get summary of user documents based on request ID",
        operation_description="Retrieve a summary of documents associated with a specific request ID.",
        manual_parameters=[
            openapi.Parameter(
                "request_id",
                openapi.IN_QUERY,
                description="The ID of the request to summarize.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: UserSummaryResponseSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
            500: "Internal Server Error",
        },
    )
    def get(self, request, format=None):
        """
        Handle GET requests for user summaries.
        """
        request_id = request.GET.get('request_id', '').strip()
        if not request_id:
            logger.warning("UserSummaryView: Missing 'request_id' parameter.")
            return Response(
                {"error": "The 'request_id' query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            summary = user_service.get_documents_summary(request_id)
            response_data = {
                "response": summary
            }
            response_serializer = UserSummaryResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"UserSummaryView: Exception occurred - {str(e)}")
            return Response(
                {"error": f"An error occurred while retrieving the summary: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
