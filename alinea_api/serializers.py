from datetime import datetime

from bson import ObjectId
from rest_framework import serializers
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    CustomUser,
)
from rest_framework import serializers

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = '__all__'

class AccessRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = '__all__'

class AccessRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequestItem
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number']

def serialize_document(doc):
    """
    Recursively serializes a MongoDB document to ensure all fields are JSON serializable.
    """
    if isinstance(doc, dict):
        return {key: serialize_document(value) for key, value in doc.items()}
    elif isinstance(doc, list):
        return [serialize_document(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)  # Convert ObjectId to string
    elif isinstance(doc, datetime):
        return doc.isoformat()  # Convert datetime to ISO format
    else:
        return doc