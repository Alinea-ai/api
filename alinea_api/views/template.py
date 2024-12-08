# yourapp/views/template.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from ..models import Template
from ..serializers import TemplateSerializer

class TemplateListCreateView(APIView):
    """
    Handle listing all templates and creating a new template.
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List Templates",
        operation_description="Retrieve a list of templates filtered by entity_id.",
        manual_parameters=[
            openapi.Parameter(
                "entity_id",
                openapi.IN_QUERY,
                description="The ID of the entity to filter templates.",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Templates retrieved successfully.",
                schema=TemplateSerializer(many=True)
            ),
            400: openapi.Response(description="Missing or invalid query parameter: 'entity_id'."),
            404: openapi.Response(description="No templates found for the given entity_id."),
            500: openapi.Response(description="Server error while retrieving templates."),
        },
    )
    def get(self, request):
        """
        Retrieve templates filtered by entity_id.
        """
        entity_id = request.query_params.get('entity_id')

        # Validate that entity_id is provided
        if not entity_id:
            return Response(
                {"error": "Missing required query parameter: 'entity_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate that entity_id is an integer
        try:
            entity_id = int(entity_id)
        except ValueError:
            return Response(
                {"error": "Invalid 'entity_id'. It must be an integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter templates by entity_id
        templates = Template.objects.filter(entity_id=entity_id)

        if not templates.exists():
            return Response(
                {"message": "No templates found for the given entity_id."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new template",
        operation_description="Create a new template with default and custom fields.",
        request_body=TemplateSerializer,
        responses={
            201: openapi.Response(
                description="Template created successfully.",
                schema=TemplateSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate template."),
            500: openapi.Response(description="Server error while creating template."),
        },
    )
    def post(self, request):
        """
        Create a new template with default and custom fields.
        """
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "A template with this entity, document type, and name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateDetailView(APIView):
    """
    Handle retrieving, updating, and deleting a specific template.
    """
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Retrieve a Template",
        operation_description="Retrieve details of a specific template by its ID.",
        responses={
            200: openapi.Response(
                description="Template retrieved successfully.",
                schema=TemplateSerializer
            ),
            404: openapi.Response(description="Template not found."),
            500: openapi.Response(description="Server error while retrieving the template."),
        },
    )
    def get(self, request, id):
        """
        Retrieve a specific template by its ID.
        """
        template = get_object_or_404(Template, id=id)
        serializer = TemplateSerializer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a Template",
        operation_description="Update an existing template by its ID.",
        request_body=TemplateSerializer,
        responses={
            200: openapi.Response(
                description="Template updated successfully.",
                schema=TemplateSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate template."),
            404: openapi.Response(description="Template not found."),
            500: openapi.Response(description="Server error while updating the template."),
        },
    )
    def put(self, request, id):
        """
        Update an existing template by its ID.
        """
        template = get_object_or_404(Template, id=id)
        serializer = TemplateSerializer(template, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(
                    {"error": "A template with this entity, document type, and name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a Template",
        operation_description="Delete a specific template by its ID.",
        responses={
            204: openapi.Response(description="Template deleted successfully."),
            404: openapi.Response(description="Template not found."),
            500: openapi.Response(description="Server error while deleting the template."),
        },
    )
    def delete(self, request, id):
        """
        Delete a specific template by its ID.
        """
        template = get_object_or_404(Template, id=id)
        try:
            template.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": "An error occurred while deleting the template."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
