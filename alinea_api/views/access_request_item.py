from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view

from alinea_api.models import AccessRequestItem, AccessRequest
from alinea_api.serializers import AccessRequestItemSerializer


class AccessRequestItemViewSet(viewsets.ModelViewSet):
    queryset = AccessRequestItem.objects.all()
    serializer_class = AccessRequestItemSerializer
    permission_classes = [permissions.IsAuthenticated]


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('access_request_id', openapi.IN_QUERY, description="ID of the access request",
                      type=openapi.TYPE_INTEGER)],
    responses={200: AccessRequestItemSerializer(many=True)})
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
        item_data = {'id': item.id, 'access_request_id': item.access_request.id,
            'data_type': item.data_type, 'data_type_display': item.get_data_type_display(),
            'status': item.status,
            'status_set_at': item.status_set_at.isoformat() if item.status_set_at else None,
            'created_at': item.created_at.isoformat() if item.created_at else None, }
        item_data_list.append(item_data)

    return JsonResponse({'items': item_data_list})


@swagger_auto_schema(method='post',
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, required=['item_id', 'status'],
        properties={'item_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                              description='ID of the AccessRequestItem'),
            'status': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='New status ("approved" or "rejected")'), }, ),
    responses={200: 'Success'})
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
