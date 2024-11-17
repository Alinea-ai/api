from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import AccessRequest, AccessRequestItem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db import transaction
import json
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=AccessRequest)
def handle_access_request_save(sender, instance, created, **kwargs):
    transaction.on_commit(lambda: send_access_request_notification(instance, created))

def send_access_request_notification(instance, created):
    if created:
        action = 'created'
        print(f'New AccessRequest created: "{instance}"')
    else:
        action = 'updated'
        print(f'AccessRequest updated: "{instance}"')
    items = AccessRequestItem.objects.filter(access_request=instance.id)
    item_data_list = []
    for item in items:
        item_data = {
            'id': item.id,
            'access_request_id': item.access_request.id,
            'data_type': item.data_type,
            'data_type_display': item.get_data_type_display(),
            'approved': item.approved,
            'approved_at': item.approved_at.isoformat() if item.approved_at else None,
        }
        item_data_list.append(item_data)

    # Prepare the message payload
    message = {
        'action': action,
        'access_request': {
            'id': instance.id,
            'entity_id': instance.entity.id,
            'entity_name': instance.entity.name,
            'user_id': instance.user.id,
            'user_username': instance.user.username,
            'requested_at': instance.requested_at.isoformat(),
            'purpose': instance.purpose,
            'items': item_data_list,
        }
    }

    # Get the user's group name
    user_id = instance.user.id
    group_name = f'user_{user_id}_group'

    # Get the channel layer
    channel_layer = get_channel_layer()

    # Send message to the user's group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'access_request_event',
            'message': json.dumps(message),
        }
    )

@receiver(pre_save, sender=AccessRequestItem)
def access_request_item_pre_save(sender, instance, **kwargs):
    if instance.pk:
        previous = AccessRequestItem.objects.get(pk=instance.pk)
        instance._previous_status = previous.status
    else:
        instance._previous_status = None

@receiver(post_save, sender=AccessRequestItem)
def handle_access_request_item_update(sender, instance, created, **kwargs):
    if not created and hasattr(instance, '_previous_status'):
        if instance.status != instance._previous_status:
            item_data = {
                'id': instance.id,
                'access_request_id': instance.access_request.id,
                'data_type': instance.data_type,
                'data_type_display': instance.get_data_type_display(),
                'status': instance.status,
                'status_set_at': instance.status_set_at.isoformat() if instance.status_set_at else None,
                'created_at': instance.created_at.isoformat() if instance.created_at else None,
            }
            message = {
                'action': 'status_updated',
                'access_request_item': item_data,
            }
            entity_id = instance.access_request.entity.id
            group_name = f'entity_{entity_id}_group'
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'access_request_item_event',
                    'message': json.dumps(message),
                }
            )
            print(f"Sent event to group: {group_name}")