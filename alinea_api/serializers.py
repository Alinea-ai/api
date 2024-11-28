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

class UserPersonalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPersonalInformation
        fields = '__all__'

class UserMedicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMedicalInfo
        fields = '__all__'

class DentalQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = DentalQuestionnaire
        fields = '__all__'

class PsychologicalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsychologicalInfo
        fields = '__all__'