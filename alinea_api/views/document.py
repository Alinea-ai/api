# views/document.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from alinea_api.models import AccessRequest, AccessRequestItem
from alinea_api.serializers import serialize_document
from alinea_api.services.documents_service import DocumentService

connection_uri = "mongodb://localhost:27017"
database_name = "users"
document_service = DocumentService(connection_uri, database_name)

class DocumentListView(APIView):
    """
    Retrieve all documents for a user or add a new document.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve documents by user ID",
        operation_description="Fetch all documents associated with a specific user ID from MongoDB.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="The ID of the user whose documents are to be fetched.",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={
            200: openapi.Response(
                "Success",
                examples={
                    "application/json": {
                        "data": {"personal_info": {"first_name": "John", "last_name": "Doe"}}
                    }
                },
            ),
            400: openapi.Response("Missing or invalid user ID."),
        },
    )
    def get(self, request, user_id):
        if not user_id:
            return Response({'error': 'Missing user_id parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        user_doc = document_service.find_user_by_user_id(user_id)
        if not user_doc:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": serialize_document(user_doc)}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Add a new document for a user",
        operation_description="Add a new document for a user. If the user doesn't exist, a new user document is created.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="The ID of the user.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "document_type",
                openapi.IN_QUERY,
                description="The type of document to add.",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["first_name", "last_name", "email"],
            example={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        ),
        responses={
            201: openapi.Response("Document added successfully."),
            400: openapi.Response("Invalid data or document type."),
        },
    )
    def post(self, request, user_id):
        """
        Adds a new document for a user in MongoDB.
        Creates a new user entry if not found.
        Expects a JSON payload with the document data.
        """
        try:
            # Convert user_id from URL parameter to integer
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Invalid user_id."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the document data is provided
        document_data = request.data
        if not document_data:
            return Response({"error": "No document data provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Get 'document_type' from query parameters
        document_type = request.query_params.get('document_type')
        if not document_type:
            return Response({"error": "document_type query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate document type
        if document_type not in document_service.VALID_DOCUMENT_TYPES:
            return Response({
                "error": f"Invalid document type. Valid types are: {', '.join(document_service.VALID_DOCUMENT_TYPES)}."},
                status=status.HTTP_400_BAD_REQUEST)

        # Find the user document
        user_doc = document_service.find_user_by_user_id(user_id)

        if not user_doc:
            # Create a new user document if not found
            try:
                new_user_doc = {"user_id": user_id, document_type: document_data}
                document_service.create_user(new_user_doc)
                return Response(
                    {"message": f"New user created and {document_type} added successfully."},
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": f"An error occurred while creating a new user document: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Add or overwrite the specific document_type field
        update_data = {document_type: document_data}

        # Update the existing user document
        try:
            updated_count = document_service.update_user(user_doc['_id'], update_data)
            if updated_count:
                return Response({"message": f"{document_type} added successfully."},
                    status=status.HTTP_201_CREATED)
            else:
                return Response({"error": f"Failed to add the {document_type} to the user's data."},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred while adding the document: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentDetailView(APIView):
    """
    Retrieve, update, or delete a specific document for a user.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve a specific document for a user",
        operation_description="Fetch a specific document type for a user.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="The ID of the user.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "document_type",
                openapi.IN_PATH,
                description="The type of document to retrieve.",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                "Success",
                examples={
                    "application/json": {
                        "data": {"personal_info": {"first_name": "John", "last_name": "Doe"}}
                    }
                },
            ),
            400: openapi.Response("Missing or invalid parameters."),
            404: openapi.Response("Document not found."),
        },
    )
    def get(self, request, user_id, document_type):
        if not user_id or not document_type:
            return Response({'error': 'Missing user_id or document_type parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        user_doc = document_service.find_user_by_user_id(user_id)
        if not user_doc:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        document = user_doc.get(document_type)
        if not document:
            return Response({'error': f'Document type "{document_type}" not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({"data": document}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a specific document for a user",
        operation_description="Update an existing document type for a user.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="The ID of the user.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "document_type",
                openapi.IN_PATH,
                description="The type of document to update.",
                type=openapi.TYPE_STRING,
            ),
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "record_id": openapi.Schema(type=openapi.TYPE_STRING),
                "description": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["description"],
            example={"record_id": "12345", "description": "Updated description"},
        ),
        responses={
            200: openapi.Response("Document updated successfully."),
            400: openapi.Response("Invalid data or document type."),
            404: openapi.Response("Document not found."),
        },
    )
    def put(self, request, user_id, document_type):
        """
        Updates an existing document in a user's data in MongoDB.
        """
        document_data = request.data  # Get the data from the request body

        # Validate that the document data is provided
        if not document_data:
            return Response({"error": "No document data provided for update."},
                status=status.HTTP_400_BAD_REQUEST)

        if document_type not in document_service.VALID_DOCUMENT_TYPES:
            return Response({
                "error": f"Invalid document type. Valid types are: {', '.join(document_service.VALID_DOCUMENT_TYPES)}."},
                status=status.HTTP_400_BAD_REQUEST)

        # Find the user document
        user_doc = document_service.find_user_by_user_id(user_id)
        if not user_doc:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # For medical_records, we'll need an identifier to update a specific record
        if document_type == 'medical_records':
            record_id = document_data.get('record_id')
            if not record_id:
                return Response({"error": "record_id is required to update a medical record."},
                    status=status.HTTP_400_BAD_REQUEST)
            # Find and update the specific medical record
            records = user_doc.get('medical_records', [])
            for idx, record in enumerate(records):
                if record.get('record_id') == record_id:
                    records[idx].update(document_data)
                    break
            else:
                return Response({"error": "Medical record not found."},
                    status=status.HTTP_404_NOT_FOUND)
            update_data = {'medical_records': records}
        else:
            # Update the specific document_type field
            update_data = {document_type: document_data}

        # Update the user document
        try:
            updated_count = document_service.update_user(user_doc['_id'], update_data)
            if updated_count:
                return Response({"message": f"{document_type} updated successfully."},
                    status=status.HTTP_200_OK)
            else:
                return Response({"error": f"No changes were made to the user's {document_type}."},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred while updating the document: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_summary="Delete a specific document for a user",
        operation_description="Deletes a specific document type for a user.",
        manual_parameters=[
            openapi.Parameter(
                "user_id",
                openapi.IN_PATH,
                description="The ID of the user.",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "document_type",
                openapi.IN_PATH,
                description="The type of document to delete.",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "record_id",
                openapi.IN_QUERY,
                description="The ID of the specific medical record to delete (required for `medical_records`).",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={
            200: openapi.Response("Document deleted successfully."),
            400: openapi.Response("Invalid data or document type."),
            404: openapi.Response("Document not found."),
        },
    )
    def delete(self, request, user_id, document_type):
        """
        Deletes a specific document from a user's data in MongoDB.
        """
        if document_type not in document_service.VALID_DOCUMENT_TYPES:
            return Response({
                "error": f"Invalid document type. Valid types are: {', '.join(document_service.VALID_DOCUMENT_TYPES)}."},
                status=status.HTTP_400_BAD_REQUEST)

        # Find the user document
        user_doc = document_service.find_user_by_user_id(user_id)
        if not user_doc:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the update data
        if document_type == 'medical_records':
            # Need to know which record to delete
            record_id = request.query_params.get('record_id')
            if not record_id:
                return Response({"error": "record_id is required to delete a medical record."},
                    status=status.HTTP_400_BAD_REQUEST)
            # Remove the specified record
            records = user_doc.get('medical_records', [])
            updated_records = [record for record in records if record.get('record_id') != record_id]
            if len(records) == len(updated_records):
                return Response({"error": "Medical record not found."},
                    status=status.HTTP_404_NOT_FOUND)
            update_data = {'medical_records': updated_records}
        else:
            # Remove the document_type field from the user document
            update_data = {document_type: None}

        # Update the user document
        try:
            updated_count = document_service.update_user(user_doc['_id'], update_data)
            if updated_count:
                return Response({"message": f"{document_type} deleted successfully."},
                    status=status.HTTP_200_OK)
            else:
                return Response({"error": f"No changes were made to the user's {document_type}."},
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error occurred while deleting the document: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentByRequestIDView(APIView):
    """
    Retrieve documents by access request ID.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve documents by access request ID",
        operation_description=(
            "Fetches all documents related to a specific access request ID. "
            "Documents are grouped by their statuses: pending, approved, and rejected."
        ),
        manual_parameters=[
            openapi.Parameter(
                "access_request_id",
                openapi.IN_PATH,
                description="The ID of the access request.",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Documents retrieved successfully.",
                examples={
                    "application/json": {
                        "data": {
                            "pending": ["data_type_1", "data_type_2"],
                            "approved": {"personal_info": {"first_name": "John", "last_name": "Doe"}},
                            "rejected": ["data_type_3"],
                        }
                    }
                },
            ),
            400: openapi.Response(description="Invalid or missing access request ID."),
            404: openapi.Response(description="Access request or user not found."),
        },
    )
    def get(self, request, access_request_id):
        if not access_request_id:
            return Response({'error': 'Missing access_request_id parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        access_request_obj = get_object_or_404(AccessRequest, id=access_request_id)
        data_by_status = {'pending': [], 'approved': [], 'rejected': []}
        access_requests = AccessRequestItem.objects.filter(access_request_id=access_request_id)

        for access_request in access_requests:
            data_by_status[access_request.status].append(access_request.data_type)
        user = access_request_obj.user
        user_doc = document_service.find_user_by_user_id(user.id)

        if not user_doc:
            return Response({"error": "User data not found in MongoDB"}, status=status.HTTP_404_NOT_FOUND)

        data = {}
        for data_type in data_by_status['approved']:
            if data_type in user_doc:
                data[data_type] = user_doc[data_type]
            else:
                data[data_type] = None
        data_by_status["approved"] = data

        return Response({"data": data_by_status}, status=status.HTTP_200_OK)
