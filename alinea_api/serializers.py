from rest_framework import serializers
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    UserPersonalInformation,
    UserMedicalInfo,
    DentalQuestionnaire,
    PsychologicalInfo,
    MedicalRecord,
)

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

