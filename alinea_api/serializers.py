# serializers.py

from datetime import datetime

from bson import ObjectId
from rest_framework import serializers
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    CustomUser, Template, Visits,
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

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'entity_id', 'document_type', 'name', 'fields', 'version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']

class VisitsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='user',
        write_only=True
    )
    entity = EntitySerializer(read_only=True)
    entity_id = serializers.PrimaryKeyRelatedField(
        queryset=Entity.objects.all(),
        source='entity',
        write_only=True
    )

    class Meta:
        model = Visits
        fields = ['id', 'user', 'user_id', 'entity', 'entity_id', 'date', 'reason', 'comments']
        read_only_fields = ['id']
