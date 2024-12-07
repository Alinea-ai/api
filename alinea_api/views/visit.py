# your_app/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # Adjust permissions as needed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from ..serializers import VisitsSerializer
from ..models import Visits


class VisitsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Visits instances.
    """
    queryset = Visits.objects.all()
    serializer_class = VisitsSerializer
    # permission_classes = [IsAuthenticated]  # Adjust based on your authentication setup

    # Optional: Override get_queryset to allow filtering by user or entity
    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        entity_id = self.request.query_params.get('entity_id')

        if user_id:
            queryset = queryset.filter(user__id=user_id)
        if entity_id:
            queryset = queryset.filter(entity__id=entity_id)
        return queryset

    # Optional: Add Swagger documentation for list, create, retrieve, update, partial_update, and destroy
    @swagger_auto_schema(
        operation_summary="List all Visits",
        operation_description="Retrieve a list of all Visits. You can filter by user_id or entity_id using query parameters.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_QUERY,
                description="Filter Visits by User ID.",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
            openapi.Parameter(
                "entity_id",
                openapi.IN_QUERY,
                description="Filter Visits by Entity ID.",
                type=openapi.TYPE_INTEGER,
                required=False,
            ),
        ],
        responses={
            200: VisitsSerializer(many=True),
            401: "Unauthorized",
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new Visit",
        operation_description="Create a new Visit instance.",
        request_body=VisitsSerializer,
        responses={
            201: VisitsSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific Visit",
        operation_description="Retrieve a Visit instance by its ID.",
        responses={
            200: VisitsSerializer(),
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a Visit",
        operation_description="Update an existing Visit instance.",
        request_body=VisitsSerializer,
        responses={
            200: VisitsSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a Visit",
        operation_description="Partially update an existing Visit instance.",
        request_body=VisitsSerializer,
        responses={
            200: VisitsSerializer(),
            400: "Bad Request",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a Visit",
        operation_description="Delete a Visit instance by its ID.",
        responses={
            204: "No Content",
            401: "Unauthorized",
            404: "Not Found",
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
