from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view

from alinea_api.models import UserPersonalInformation, UserMedicalInfo, DentalQuestionnaire, \
    PsychologicalInfo, AccessRequest, AccessRequestItem
from alinea_api.serializers import UserPersonalInformationSerializer, UserMedicalInfoSerializer, \
    DentalQuestionnaireSerializer, PsychologicalInfoSerializer


@api_view(['GET'])
def get_documents(request, access_request_id):
    DATA_TYPE_MODEL_SERIALIZER_MAP = {
        'personal_info': (UserPersonalInformation, UserPersonalInformationSerializer),
        'medical_info': (UserMedicalInfo, UserMedicalInfoSerializer),
        'dental_info': (DentalQuestionnaire, DentalQuestionnaireSerializer),
        'psychological_info': (PsychologicalInfo, PsychologicalInfoSerializer), }
    if not access_request_id:
        return HttpResponseBadRequest('Missing access_request_id parameter.')
    access_request_obj = AccessRequest.objects.get(id=access_request_id)
    if not access_request_obj:
        return HttpResponseBadRequest('Request not found')
    data_by_status = {'pending': [], 'approved': [], 'rejected': [], }
    access_requests = AccessRequestItem.objects.filter(access_request_id=access_request_id)
    for access_request in access_requests:
        data_by_status[access_request.status].append(access_request.data_type)
    user = access_request_obj.user
    data = {}
    for data_type in data_by_status['approved']:
        model_class, serializer_class = DATA_TYPE_MODEL_SERIALIZER_MAP.get(data_type)
        if model_class and serializer_class:
            try:
                instance = model_class.objects.get(user_id=user.id)
                serializer = serializer_class(instance)
                data[data_type] = serializer.data
            except model_class.DoesNotExist:
                data[data_type] = None
    data_by_status["approved"] = data
    return JsonResponse({"data": data_by_status})
