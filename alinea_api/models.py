from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.conf import settings


ENTITY_TYPE_CHOICES = [
    ('clinic', 'Clinic'),
    ('dentist', 'Dentist'),
    ('hospital', 'Hospital'),
    ('psychologist', 'Psychologist'),
    ('therapist', 'Therapist'),
    ('pharmacy', 'Pharmacy'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
DOCUMENT_TYPE_CHOICES = [
    ('personal_info', 'Personal Information'),
    ('medical_info', 'Medical Information'),
    ('dental', 'Dental Questionnaire'),
    ('psychological_info', 'Psychological Information'),
]

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='customuser'
    )


class Entity(models.Model):
    name = models.CharField(max_length=255)
    entity_type = models.CharField(
        max_length=50,
        choices=ENTITY_TYPE_CHOICES,
        blank=False
    )
    address = models.TextField(blank=True)
    street_name = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    timezone = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_entity_type_display()})"


class AccessRequest(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"AccessRequest by {self.entity} for {self.user}"


class AccessRequestItem(models.Model):
    access_request = models.ForeignKey(AccessRequest, on_delete=models.CASCADE, related_name='items')
    data_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    status_set_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(null=True, blank=True)


class Visits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True)
    comments = models.TextField(blank=True)

class Template(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='templates')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    fields = models.JSONField()
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('entity', 'document_type', 'name')

    def __str__(self):
        return f"{self.entity.name} - {self.document_type} (v{self.version})"

class DefaultField(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('personal_info', 'Personal Information'),
        ('medical_info', 'Medical Information'),
        ('dental', 'Dental Questionnaire'),
        ('psychological_info', 'Psychological Information'),
    ]

    FIELD_TYPE_CHOICES = [
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
    ]

    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)  # To maintain the order of fields

    class Meta:
        unique_together = ('document_type', 'field_name')

    def __str__(self):
        return f"{self.field_name} ({self.document_type})"


class UserTemplateAssignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='template_assignments')
    template = models.ForeignKey('Template', on_delete=models.CASCADE,
                                 related_name='user_assignments')
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='user_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')

    class Meta:
        unique_together = ('user', 'template', 'entity')  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.template.name} assigned to {self.user.username} ({self.entity.name})"