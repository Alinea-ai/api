from django.core.management.base import BaseCommand

from alinea_api.models import DefaultField


class Command(BaseCommand):
    help = "Populate the DefaultField table with default fields for various document types"

    def handle(self, *args, **kwargs):
        # Data to populate
        data = [
            # Personal Info
            {'document_type': 'personal_info', 'field_name': 'first_name', 'field_type': 'string',
             'required': True, 'order': 1},
            {'document_type': 'personal_info', 'field_name': 'last_name', 'field_type': 'string',
             'required': True, 'order': 2},
            {'document_type': 'personal_info', 'field_name': 'date_of_birth', 'field_type': 'date',
             'required': True, 'order': 3},
            {'document_type': 'personal_info', 'field_name': 'gender', 'field_type': 'string',
             'required': True, 'order': 4},
            {'document_type': 'personal_info', 'field_name': 'address', 'field_type': 'string',
             'required': True, 'order': 5},
            {'document_type': 'personal_info', 'field_name': 'phone_number', 'field_type': 'string',
             'required': True, 'order': 6},
            {'document_type': 'personal_info', 'field_name': 'email', 'field_type': 'string',
             'required': True, 'order': 7},
            {'document_type': 'personal_info', 'field_name': 'emergency_contact_name',
             'field_type': 'string', 'required': True, 'order': 8},
            {'document_type': 'personal_info', 'field_name': 'emergency_contact_phone',
             'field_type': 'string', 'required': True, 'order': 9},
            {'document_type': 'personal_info', 'field_name': 'insurance_provider',
             'field_type': 'string', 'required': False, 'order': 10},
            {'document_type': 'personal_info', 'field_name': 'insurance_policy_number',
             'field_type': 'string', 'required': False, 'order': 11},

            # Medical Info
            {'document_type': 'medical_info', 'field_name': 'allergies', 'field_type': 'string',
             'required': False, 'order': 1},
            {'document_type': 'medical_info', 'field_name': 'current_medications',
             'field_type': 'string', 'required': False, 'order': 2},
            {'document_type': 'medical_info', 'field_name': 'past_surgeries',
             'field_type': 'string', 'required': False, 'order': 3},
            {'document_type': 'medical_info', 'field_name': 'chronic_conditions',
             'field_type': 'string', 'required': False, 'order': 4},
            {'document_type': 'medical_info', 'field_name': 'family_medical_history',
             'field_type': 'string', 'required': False, 'order': 5},
            {'document_type': 'medical_info', 'field_name': 'immunizations', 'field_type': 'string',
             'required': False, 'order': 6},
            {'document_type': 'medical_info', 'field_name': 'smoking_status',
             'field_type': 'string', 'required': False, 'order': 7},
            {'document_type': 'medical_info', 'field_name': 'alcohol_use', 'field_type': 'string',
             'required': False, 'order': 8},
            {'document_type': 'medical_info', 'field_name': 'exercise_frequency',
             'field_type': 'string', 'required': False, 'order': 9},
            {'document_type': 'medical_info', 'field_name': 'height_cm', 'field_type': 'float',
             'required': False, 'order': 10},
            {'document_type': 'medical_info', 'field_name': 'weight_kg', 'field_type': 'float',
             'required': False, 'order': 11},
            {'document_type': 'medical_info', 'field_name': 'blood_type', 'field_type': 'string',
             'required': False, 'order': 12},

            # Dental Info
            {'document_type': 'dental', 'field_name': 'last_dental_visit', 'field_type': 'date',
             'required': False, 'order': 1},
            {'document_type': 'dental', 'field_name': 'reason_for_last_visit',
             'field_type': 'string', 'required': False, 'order': 2},
            {'document_type': 'dental', 'field_name': 'brushing_frequency', 'field_type': 'string',
             'required': False, 'order': 3},
            {'document_type': 'dental', 'field_name': 'flossing_frequency', 'field_type': 'string',
             'required': False, 'order': 4},
            {'document_type': 'dental', 'field_name': 'any_dental_pain', 'field_type': 'boolean',
             'required': False, 'order': 5},
            {'document_type': 'dental', 'field_name': 'sensitivity_to_hot_or_cold',
             'field_type': 'boolean', 'required': False, 'order': 6},
            {'document_type': 'dental', 'field_name': 'previous_dental_procedures',
             'field_type': 'string', 'required': False, 'order': 7},
            {'document_type': 'dental', 'field_name': 'bleeding_gums', 'field_type': 'boolean',
             'required': False, 'order': 8},
            {'document_type': 'dental', 'field_name': 'teeth_grinding', 'field_type': 'boolean',
             'required': False, 'order': 9},
            {'document_type': 'dental', 'field_name': 'jaw_pain', 'field_type': 'boolean',
             'required': False, 'order': 10},

            # Psychological Info
            {'document_type': 'psychological_info', 'field_name': 'current_mood',
             'field_type': 'string', 'required': False, 'order': 1},
            {'document_type': 'psychological_info', 'field_name': 'stress_level',
             'field_type': 'integer', 'required': False, 'order': 2},
            {'document_type': 'psychological_info', 'field_name': 'sleep_quality',
             'field_type': 'integer', 'required': False, 'order': 3},
            {'document_type': 'psychological_info', 'field_name': 'past_mental_health_issues',
             'field_type': 'string', 'required': False, 'order': 4},
            {'document_type': 'psychological_info', 'field_name': 'current_therapy',
             'field_type': 'boolean', 'required': False, 'order': 5},
            {'document_type': 'psychological_info', 'field_name': 'medications',
             'field_type': 'string', 'required': False, 'order': 6},
            {'document_type': 'psychological_info', 'field_name': 'any_suicidal_thoughts',
             'field_type': 'boolean', 'required': False, 'order': 7},
            {'document_type': 'psychological_info', 'field_name': 'anxiety_level',
             'field_type': 'integer', 'required': False, 'order': 8},
            {'document_type': 'psychological_info', 'field_name': 'history_of_substance_abuse',
             'field_type': 'string', 'required': False, 'order': 9},
            {'document_type': 'psychological_info', 'field_name': 'support_system',
             'field_type': 'string', 'required': False, 'order': 10},
        ]

        # Insert data into the database
        for entry in data:
            DefaultField.objects.get_or_create(**entry)

        self.stdout.write(self.style.SUCCESS('Default fields have been populated successfully!'))
