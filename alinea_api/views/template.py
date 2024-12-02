from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db import IntegrityError

from alinea_api.models import Template, DefaultField


@api_view(['POST'])
def create_template(request):
    """
    Create a new template with default fields included.
    """
    data = request.data

    # Validate input
    required_fields = ['entity_id', 'document_type', 'custom_fields', 'name']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return HttpResponseBadRequest(f"Missing required fields: {', '.join(missing_fields)}")

    entity_id = data['entity_id']
    document_type = data['document_type']
    custom_fields = data.get('custom_fields', [])
    name = data['name']

    # Retrieve default fields for the document_type
    default_fields = DefaultField.objects.filter(document_type=document_type).values(
        'field_name', 'field_type', 'required', 'order'
    )

    if not default_fields.exists():
        return HttpResponseBadRequest(f"No default fields found for document type '{document_type}'.")

    # Combine default fields and custom fields
    all_fields = list(default_fields)
    for custom_field in custom_fields:
        if 'field_name' not in custom_field or 'field_type' not in custom_field:
            return HttpResponseBadRequest("Each custom field must include 'field_name' and 'field_type'.")
        all_fields.append(custom_field)

    # Ensure unique field names
    field_names = [field['field_name'] for field in all_fields]
    if len(field_names) != len(set(field_names)):
        return HttpResponseBadRequest("Duplicate field names are not allowed in template fields.")

    # Create the template
    try:
        template = Template.objects.create(
            entity_id=entity_id,
            document_type=document_type,
            fields=all_fields,
            name=name,
        )
    except IntegrityError:
        return HttpResponseBadRequest("A template with this entity, document type, and version already exists.")

    return Response({
        "message": "Template created successfully.",
        "template_id": template.id,
        "fields": template.fields,
    })


@api_view(['GET'])
def get_templates_by_entity(request):
    """
    Retrieve templates filtered by entity_id.
    """
    entity_id = request.query_params.get('entity_id')

    # Validate that entity_id is provided
    if not entity_id:
        return HttpResponseBadRequest("Missing required query parameter: 'entity_id'")

    # Filter templates by entity_id
    templates = Template.objects.filter(entity_id=entity_id)

    if not templates.exists():
        return Response({"message": "No templates found for the given entity_id."}, status=404)

    # Serialize the templates
    template_list = [
        {
            "id": template.id,
            "name": template.name,
            "document_type": template.document_type,
            "fields": template.fields,
            "version": template.version,
            "created_at": template.created_at,
            "updated_at": template.updated_at,
        }
        for template in templates
    ]

    return Response(template_list)
