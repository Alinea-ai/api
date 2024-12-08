# serializers.py

from datetime import datetime

from bson import ObjectId
from rest_framework import serializers
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    CustomUser, Template, Visits, DefaultField, UserTemplateAssignment,
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

class DefaultFieldSerializer(serializers.Serializer):
    field_name = serializers.CharField()
    field_type = serializers.CharField()
    required = serializers.BooleanField(default=False)
    order = serializers.IntegerField(required=False)

class DefaultFieldGroupedSerializer(serializers.Serializer):
    document_type = serializers.ChoiceField(choices=DefaultField.DOCUMENT_TYPE_CHOICES)
    fields = DefaultFieldSerializer(many=True)



class FieldSerializer(serializers.Serializer):
    field_name = serializers.CharField(max_length=100)
    field_type = serializers.ChoiceField(choices=[
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
        ('email', 'Email'),
        ('tel', 'Telephone'),
        ('password', 'Password'),
    ])
    required = serializers.BooleanField(default=False)
    order = serializers.IntegerField(required=False)

    def validate_field_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Field name cannot be empty.")
        return value

class TemplateSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Template
        fields = ['id', 'entity', 'document_type', 'name', 'fields', 'version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        template = Template.objects.create(**validated_data, fields=fields_data)
        return template

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)

        # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update 'fields' JSONField if provided
        if fields_data is not None:
            # Optionally, you can implement more complex update logic here
            instance.fields = fields_data

        instance.save()
        return instance


class UserTemplateAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    template = TemplateSerializer(read_only=True)
    entity = EntitySerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True,
                                                 source='user')
    template_id = serializers.PrimaryKeyRelatedField(queryset=Template.objects.all(),
                                                     write_only=True, source='template')
    entity_id = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.all(), write_only=True,
                                                   source='entity')

    class Meta:
        model = UserTemplateAssignment
        fields = ['id', 'user', 'template', 'entity', 'user_id', 'template_id', 'entity_id',
                  'assigned_at', 'status']
        read_only_fields = ['id', 'assigned_at']
