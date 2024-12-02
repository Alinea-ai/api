from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from alinea_api.models import AccessRequest, AccessRequestItem
from alinea_api.serializers import serialize_document
from alinea_api.services.documents_service import DocumentService

connection_uri = "mongodb://localhost:27017"
database_name = "users"
document_service = DocumentService(connection_uri, database_name)


@api_view(['GET'])
def get_documents(request, user_id):
    if not user_id:
        return HttpResponseBadRequest('Missing user_id parameter.')
    user_doc = document_service.find_user_by_user_id(user_id)
    if not user_doc:
        return HttpResponseBadRequest('User does not exist.')

    return JsonResponse({"data": serialize_document(user_doc)})


@api_view(['GET'])
def get_documents_by_request_id(request, access_request_id):
    if not access_request_id:
        return HttpResponseBadRequest('Missing access_request_id parameter.')
    access_request_obj = get_object_or_404(AccessRequest, id=access_request_id)
    data_by_status = {'pending': [], 'approved': [], 'rejected': []}
    access_requests = AccessRequestItem.objects.filter(access_request_id=access_request_id)

    for access_request in access_requests:
        data_by_status[access_request.status].append(access_request.data_type)
    user = access_request_obj.user
    user_doc = document_service.find_user_by_user_id(user.id)

    if not user_doc:
        return JsonResponse({"error": "User data not found in MongoDB"}, status=404)

    data = {}
    for data_type in data_by_status['approved']:
        if data_type in user_doc:
            data[data_type] = user_doc[data_type]
        else:
            data[data_type] = None
    data_by_status["approved"] = data

    return JsonResponse({"data": data_by_status})


@api_view(['POST'])
def add_document(request, user_id, document_type):
    """
    Adds or updates a document for a user in MongoDB.
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
        print(">" * 50, updated_count)
        if updated_count:
            return Response({"message": f"{document_type} added successfully."},
                status=status.HTTP_201_CREATED)
        else:
            return Response({"error": f"Failed to add the {document_type} to the user's data."},
                status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"An error occurred while adding the document: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_document(request, username, document_type):
    """
    Updates an existing document in a user's data in MongoDB.
    Expects a JSON payload with the updated document data.
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
    user_doc = document_service.find_document({"username": username})
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


@api_view(['DELETE'])
def delete_document(request, username, document_type):
    """
    Deletes a document from a user's data in MongoDB.
    For medical_records, expects 'record_id' in the query parameters.
    """
    # Validate that the document_type is valid

    if document_type not in document_service.VALID_DOCUMENT_TYPES:
        return Response({
            "error": f"Invalid document type. Valid types are: {', '.join(document_service.VALID_DOCUMENT_TYPES)}."},
            status=status.HTTP_400_BAD_REQUEST)

    # Find the user document
    user_doc = document_service.find_document({"username": username})
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
