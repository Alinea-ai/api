from django.db import models
from django.contrib.auth.models import User

SMOKING_STATUS_CHOICES = [
    ('never_smoked', 'Never Smoked'),
    ('former_smoker', 'Former Smoker'),
    ('current_smoker', 'Current Smoker'),
]

ALCOHOL_CONSUMPTION_CHOICES = [
    ('none', 'None'),
    ('social_drinker', 'Social Drinker'),
    ('regular_drinker', 'Regular Drinker'),
    ('heavy_drinker', 'Heavy Drinker'),
]

EXERCISE_FREQUENCY_CHOICES = [
    ('none', 'None'),
    ('occasional', 'Occasional'),
    ('regular', 'Regular'),
    ('frequent', 'Frequent'),
]

ENTITY_TYPE_CHOICES = [
    ('clinic', 'Clinic'),
    ('dentist', 'Dentist'),
    ('hospital', 'Hospital'),
    ('psychologist', 'Psychologist'),
    ('therapist', 'Therapist'),
    ('pharmacy', 'Pharmacy'),
]

MOOD_CHOICES = [
    ('stable', 'Stable'),
    ('anxious', 'Anxious'),
    ('depressed', 'Depressed'),
    ('irritable', 'Irritable'),
    ('elevated', 'Elevated'),
]

DATA_TYPE_CHOICES = [
    ('personal_info', 'Personal Information'),
    ('medical_info', 'Medical Information'),
    ('dental_questionnaire', 'Dental Questionnaire'),
    ('psychological_info', 'Psychological Information'),
]


class Entity(models.Model):
    name = models.CharField(max_length=255)
    entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPE_CHOICES,
        blank=False
    )
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"


class AccessRequest(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"AccessRequest by {self.entity} for {self.user}"


STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class AccessRequestItem(models.Model):
    access_request = models.ForeignKey(AccessRequest, on_delete=models.CASCADE, related_name='items')
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_set_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(null=True, blank=True)


class UserPersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Personal Information"


class UserMedicalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    allergies = models.TextField(blank=True)
    surgeries = models.TextField(blank=True)
    smoking_status = models.CharField(
        max_length=15,
        choices=SMOKING_STATUS_CHOICES,
        blank=True
    )
    alcohol_consumption = models.CharField(
        max_length=20,
        choices=ALCOHOL_CONSUMPTION_CHOICES,
        blank=True
    )
    exercise_frequency = models.CharField(
        max_length=15,
        choices=EXERCISE_FREQUENCY_CHOICES,
        blank=True
    )
    medications = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    family_medical_history = models.TextField(blank=True)
    immunizations = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Medical Information"

class DentalQuestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_dental_visit = models.DateField(null=True, blank=True)
    reason_for_last_visit = models.CharField(max_length=255, blank=True)
    brushing_frequency = models.CharField(max_length=50, blank=True)
    flossing_frequency = models.CharField(max_length=50, blank=True)
    dental_issues = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Dental Questionnaire"

class PsychologicalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        blank=True
    )
    stress_level = models.IntegerField(
        null=True,
        blank=True,
        help_text="Scale from 1 (low stress) to 10 (high stress)"
    )
    sleep_quality = models.IntegerField(
        null=True,
        blank=True,
        help_text="Scale from 1 (poor sleep) to 10 (excellent sleep)"
    )
    mental_health_history = models.TextField(
        blank=True,
        help_text="Past mental health diagnoses or treatments"
    )
    current_symptoms = models.TextField(
        blank=True,
        help_text="Current mental health symptoms"
    )
    therapy_history = models.TextField(
        blank=True,
        help_text="Previous therapy or counseling experiences"
    )
    medications = models.TextField(
        blank=True,
        help_text="Current psychiatric medications"
    )

    def __str__(self):
        return f"{self.user.username}'s Psychological Information"

class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='medical_records/', blank=True)

    def __str__(self):
        return f"{self.record_type} for {self.user.username} on {self.date}"
