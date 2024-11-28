from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from drf_yasg import openapi
from rest_framework.response import Response

from .models import (Entity, AccessRequest, AccessRequestItem, UserPersonalInformation,
                     UserMedicalInfo, PsychologicalInfo, DentalQuestionnaire, )
from .serializers import (EntitySerializer, AccessRequestSerializer, AccessRequestItemSerializer,
                          UserPersonalInformationSerializer, UserMedicalInfoSerializer,
                          DentalQuestionnaireSerializer, PsychologicalInfoSerializer, )


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [permissions.IsAuthenticated]

class AccessRequestViewSet(viewsets.ModelViewSet):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(entity=self.request.user.entity)

class AccessRequestItemViewSet(viewsets.ModelViewSet):
    queryset = AccessRequestItem.objects.all()
    serializer_class = AccessRequestItemSerializer
    permission_classes = [permissions.IsAuthenticated]

def websocket_test(request):
    return render(request, 'doctor_dashboard.html')

def access_requests_view(request):
    return render(request, 'user_dashboard.html')

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['item_id', 'status'],
        properties={
            'item_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the AccessRequestItem'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='New status ("approved" or "rejected")'),
        },
    ),
    responses={200: 'Success'}
)
@api_view(['POST'])
@csrf_exempt
def set_access_request_item_status(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        status = request.POST.get('status')

        if not item_id or not status:
            return JsonResponse({'status': 'error', 'message': 'Item ID and status are required.'})

        if status not in ['approved', 'rejected']:
            return JsonResponse({'status': 'error', 'message': 'Invalid status.'})

        try:
            item = AccessRequestItem.objects.get(id=item_id)
            item.status = status
            item.status_set_at = timezone.now()
            item.save()
            return JsonResponse({'status': 'success'})
        except AccessRequestItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'AccessRequestItem not found.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('access_request_id', openapi.IN_QUERY, description="ID of the access request", type=openapi.TYPE_INTEGER)
    ],
    responses={200: AccessRequestItemSerializer(many=True)}
)
@api_view(['GET'])
def get_access_request_items(request):
    access_request_id = request.GET.get('access_request_id')

    if not access_request_id:
        return HttpResponseBadRequest('Missing access_request_id parameter.')

    try:
        access_request = AccessRequest.objects.get(id=access_request_id)
    except AccessRequest.DoesNotExist:
        return JsonResponse({'error': 'AccessRequest not found.'}, status=404)

    items = AccessRequestItem.objects.filter(access_request=access_request)

    item_data_list = []
    for item in items:
        item_data = {
            'id': item.id,
            'access_request_id': item.access_request.id,
            'data_type': item.data_type,
            'data_type_display': item.get_data_type_display(),
            'status': item.status,
            'status_set_at': item.status_set_at.isoformat() if item.status_set_at else None,
            'created_at': item.created_at.isoformat() if item.created_at else None,
        }
        item_data_list.append(item_data)

    return JsonResponse({'items': item_data_list})

@api_view(['GET'])
def get_documents(request, access_request_id):
    DATA_TYPE_MODEL_SERIALIZER_MAP = {
        'personal_info': (UserPersonalInformation, UserPersonalInformationSerializer),
        'medical_info': (UserMedicalInfo, UserMedicalInfoSerializer),
        'dental_info': (DentalQuestionnaire, DentalQuestionnaireSerializer),
        'psychological_info': (PsychologicalInfo, PsychologicalInfoSerializer),
    }
    if not access_request_id:
        return HttpResponseBadRequest('Missing access_request_id parameter.')
    access_request_obj =  AccessRequest.objects.get(id=access_request_id)
    if not access_request_obj:
        return HttpResponseBadRequest('Request not found')
    data_by_status = {
        'pending': [],
        'approved': [],
        'rejected': [],
    }
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






