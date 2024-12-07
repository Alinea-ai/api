# views/template.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from alinea_api.models import Template, DefaultField
from alinea_api.serializers import TemplateSerializer  # We'll define this serializer below

class TemplateView(APIView):
    """
    Handle creation and retrieval of templates.
    """

    @swagger_auto_schema(
        operation_summary="Create a new template",
        operation_description="Create a new template with default fields included.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['entity_id', 'document_type', 'name'],
            properties={
                "entity_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the entity."),
                "document_type": openapi.Schema(type=openapi.TYPE_STRING, description="Type of the document."),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the template."),
                "custom_fields": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "field_name": openapi.Schema(type=openapi.TYPE_STRING, description="Name of the field."),
                            "field_type": openapi.Schema(type=openapi.TYPE_STRING, description="Type of the field."),
                        },
                        required=["field_name", "field_type"]
                    ),
                    description="List of custom fields to include in the template."
                ),
            },
            example={
                "entity_id": 1,
                "document_type": "invoice",
                "name": "Standard Invoice Template",
                "custom_fields": [
                    {"field_name": "discount", "field_type": "float"},
                    {"field_name": "tax", "field_type": "float"}
                ]
            },
        ),
        responses={
            201: openapi.Response(
                description="Template created successfully.",
                examples={
                    "application/json": {
                        "message": "Template created successfully.",
                        "template_id": 123,
                        "fields": [
                            {"field_name": "first_name", "field_type": "string", "required": True, "order": 1},
                            {"field_name": "last_name", "field_type": "string", "required": True, "order": 2},
                            {"field_name": "email", "field_type": "string", "required": False, "order": 3},
                            {"field_name": "discount", "field_type": "float", "required": False, "order": 4},
                            {"field_name": "tax", "field_type": "float", "required": False, "order": 5},
                        ],
                    }
                },
            ),
            400: openapi.Response(description="Invalid input or duplicate template."),
            500: openapi.Response(description="Server error while creating template."),
        },
    )
    def post(self, request):
        """
        Create a new template with default fields included.
        """
        data = request.data

        # Validate input
        required_fields = ['entity_id', 'document_type', 'name']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(
                {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        entity_id = data['entity_id']
        document_type = data['document_type']
        custom_fields = data.get('custom_fields', [])
        name = data['name']

        # Retrieve default fields for the document_type
        default_fields_qs = DefaultField.objects.filter(document_type=document_type).values(
            'field_name', 'field_type', 'required', 'order'
        )

        if not default_fields_qs.exists():
            return Response(
                {"error": f"No default fields found for document type '{document_type}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        default_fields = list(default_fields_qs)

        # Combine default fields and custom fields
        all_fields = default_fields.copy()
        for custom_field in custom_fields:
            if 'field_name' not in custom_field or 'field_type' not in custom_field:
                return Response(
                    {"error": "Each custom field must include 'field_name' and 'field_type'."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            all_fields.append(custom_field)

        # Ensure unique field names
        field_names = [field['field_name'] for field in all_fields]
        if len(field_names) != len(set(field_names)):
            return Response(
                {"error": "Duplicate field names are not allowed in template fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional: Sort fields based on 'order' if applicable
        all_fields_sorted = sorted(all_fields, key=lambda x: x.get('order', 0))

        # Create the template
        try:
            template = Template.objects.create(
                entity_id=entity_id,
                document_type=document_type,
                fields=all_fields_sorted,
                name=name,
            )
        except IntegrityError:
            return Response(
                {"error": "A template with this entity, document type, and name already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            "message": "Template created successfully.",
            "template_id": template.id,
            "fields": template.fields,
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Retrieve templates by entity ID",
        operation_description="Retrieve templates filtered by entity_id.",
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
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Standard Invoice Template",
                            "document_type": "invoice",
                            "fields": [
                                {"field_name": "first_name", "field_type": "string", "required": True, "order": 1},
                                {"field_name": "last_name", "field_type": "string", "required": True, "order": 2},
                                {"field_name": "email", "field_type": "string", "required": False, "order": 3},
                                {"field_name": "discount", "field_type": "float", "required": False, "order": 4},
                                {"field_name": "tax", "field_type": "float", "required": False, "order": 5},
                            ],
                            "version": 1,
                            "created_at": "2024-04-27T12:34:56Z",
                            "updated_at": "2024-04-27T12:34:56Z",
                        },
                        # More templates...
                    ]
                },
            ),
            400: openapi.Response(description="Missing required query parameter: 'entity_id'."),
            404: openapi.Response(description="No templates found for the given entity_id."),
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

        # Optionally, validate that entity_id is an integer
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

        # Serialize the templates using a serializer
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
