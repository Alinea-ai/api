# yourapp/views/default_fields.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from alinea_api.models import DefaultField
from alinea_api.serializers import DefaultFieldSerializer, DefaultFieldGroupedSerializer


class DefaultFieldListCreateView(APIView):
    """
    Handle listing all DefaultField instances and creating a new DefaultField.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List all Default Fields",
        operation_description="Retrieve a list of all default fields. Optionally filter by document_type.",
        manual_parameters=[
            openapi.Parameter(
                "document_type",
                openapi.IN_QUERY,
                description="Filter fields by document type.",
                type=openapi.TYPE_STRING,
                required=False,
                enum=[choice[0] for choice in DefaultField.DOCUMENT_TYPE_CHOICES],
            ),
        ],
        responses={
            200: openapi.Response(
                description="A list of default fields.",
                schema=DefaultFieldSerializer(many=True)
            )
        }
    )
    def get(self, request):
        """
        Retrieve a list of all DefaultField instances.
        Optionally filter by document_type using query parameters.
        """
        document_type = request.query_params.get('document_type', None)
        default_fields = DefaultField.objects.all().order_by('order')

        if document_type:
            if document_type not in dict(DefaultField.DOCUMENT_TYPE_CHOICES):
                return Response(
                    {"error": f"Invalid document_type. Available types: {', '.join(dict(DefaultField.DOCUMENT_TYPE_CHOICES).keys())}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            default_fields = default_fields.filter(document_type=document_type)

        serializer = DefaultFieldSerializer(default_fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new Default Field",
        operation_description="Create a new default field with the specified details.",
        request_body=DefaultFieldSerializer,
        responses={
            201: openapi.Response(
                description="Default field created successfully.",
                schema=DefaultFieldSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate field."),
            500: openapi.Response(description="Server error while creating default field."),
        },
    )
    def post(self, request):
        """
        Create a new DefaultField instance.
        """
        serializer = DefaultFieldSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"error": "A default field with this document type and field name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DefaultFieldDetailView(APIView):
    """
    Handle retrieval, update, and deletion of a specific DefaultField instance.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Retrieve a Default Field",
        operation_description="Retrieve details of a specific default field by its ID.",
        responses={
            200: openapi.Response(
                description="Default field retrieved successfully.",
                schema=DefaultFieldSerializer
            ),
            404: openapi.Response(description="Default field not found."),
        },
    )
    def get(self, request, pk):
        """
        Retrieve a specific DefaultField instance by its ID.
        """
        default_field = get_object_or_404(DefaultField, pk=pk)
        serializer = DefaultFieldSerializer(default_field)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a Default Field",
        operation_description="Update details of a specific default field by its ID.",
        request_body=DefaultFieldSerializer,
        responses={
            200: openapi.Response(
                description="Default field updated successfully.",
                schema=DefaultFieldSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate field."),
            404: openapi.Response(description="Default field not found."),
            500: openapi.Response(description="Server error while updating default field."),
        },
    )
    def put(self, request, pk):
        """
        Update a specific DefaultField instance by its ID.
        """
        default_field = get_object_or_404(DefaultField, pk=pk)
        serializer = DefaultFieldSerializer(default_field, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(
                    {"error": "A default field with this document type and field name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partial Update a Default Field",
        operation_description="Partially update details of a specific default field by its ID.",
        request_body=DefaultFieldSerializer,
        responses={
            200: openapi.Response(
                description="Default field updated successfully.",
                schema=DefaultFieldSerializer
            ),
            400: openapi.Response(description="Invalid input or duplicate field."),
            404: openapi.Response(description="Default field not found."),
            500: openapi.Response(description="Server error while updating default field."),
        },
    )
    def patch(self, request, pk):
        """
        Partially update a specific DefaultField instance by its ID.
        """
        default_field = get_object_or_404(DefaultField, pk=pk)
        serializer = DefaultFieldSerializer(default_field, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except IntegrityError:
                return Response(
                    {"error": "A default field with this document type and field name already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete a Default Field",
        operation_description="Delete a specific default field by its ID.",
        responses={
            204: openapi.Response(description="Default field deleted successfully."),
            404: openapi.Response(description="Default field not found."),
            500: openapi.Response(description="Server error while deleting default field."),
        },
    )
    def delete(self, request, pk):
        """
        Delete a specific DefaultField instance by its ID.
        """
        default_field = get_object_or_404(DefaultField, pk=pk)
        try:
            default_field.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"error": "An error occurred while deleting the default field."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DefaultFieldGroupedByTypeView(APIView):
    """
    Handle retrieval of all DefaultField instances grouped by their document_type.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List Default Fields Grouped by Document Type",
        operation_description="Retrieve all default fields grouped by their document type.",
        responses={
            200: openapi.Response(
                description="Default fields grouped by document type.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        doc_type: openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT,ref='#/definitions/DefaultFieldSerializer')
                        ) for doc_type, _ in DefaultField.DOCUMENT_TYPE_CHOICES
                    }
                )
            ),
            404: openapi.Response(description="No default fields found."),
        },
    )
    def get(self, request):
        """
        Retrieve all DefaultField instances grouped by their document_type.
        """
        default_fields = DefaultField.objects.all().order_by('document_type', 'order')
        if not default_fields.exists():
            return Response(
                {"message": "No default fields found."},
                status=status.HTTP_404_NOT_FOUND
            )

        grouped_fields = {}
        for doc_type, _ in DefaultField.DOCUMENT_TYPE_CHOICES:
            fields = default_fields.filter(document_type=doc_type)
            if fields.exists():
                serializer = DefaultFieldSerializer(fields, many=True)
                grouped_fields[doc_type] = serializer.data

        return Response(grouped_fields, status=status.HTTP_200_OK)
