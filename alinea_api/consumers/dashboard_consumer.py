import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from alinea_api.models import Entity, AccessRequest, AccessRequestItem, CustomUser


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("WebSocket connect")
        entity = await self.get_dummy_entity()
        self.entity_id = entity.id
        self.group_name = f'entity_{self.entity_id}_group'

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket'}))
        print(f"Added to group: {self.group_name}")


    async def disconnect(self, close_code):
        print(f"WebSocket disconnect: {close_code}")

        # Remove the channel from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print(f"Removed from group: {self.group_name}")


    async def receive(self, text_data):
        print(f"WebSocket receive: {text_data}")
        data = json.loads(text_data)

        if 'selected_data_types' in data:
            selected_data_types = data['selected_data_types']
            # Get the authenticated user
            user = await self.get_dummy_user()
            entity = await self.get_dummy_entity()

            # Create AccessRequest
            access_request = await database_sync_to_async(AccessRequest.objects.create)(entity=entity,
                user=user, purpose='Requested via WebSocket')

            # Create AccessRequestItems
            for data_type in selected_data_types:
                await database_sync_to_async(AccessRequestItem.objects.create)(
                    access_request=access_request, data_type=data_type)

            # Prepare response
            response = {'message': 'AccessRequest and AccessRequestItems created successfully.',
                'access_request_id': access_request.id, 'selected_data_types': selected_data_types}
            await self.send(text_data=json.dumps(response))
            print(f"Created AccessRequest {access_request.id} for user {user.username}")

        else:
            response = {'error': 'Invalid data received.'}
            await self.send(text_data=json.dumps(response))
            print("Invalid data received.")


    async def access_request_item_event(self, event):
        # Handle the event sent to the group
        message = event['message']
        await self.send(text_data=message)
        print(f"Event received: {message}")


    @database_sync_to_async
    def get_dummy_user(self):
        # Get or create a dummy user with pk=1
        try:
            user = CustomUser.objects.get(pk=1)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(username='dummyuser', password='password')
            print("Created dummy user.")
        return user


    @database_sync_to_async
    def get_dummy_entity(self):
        # Get or create a dummy entity with pk=1
        try:
            entity = Entity.objects.get(pk=1)
        except Entity.DoesNotExist:
            entity = Entity.objects.create(name='Dummy Entity')
            print("Created dummy entity.")
        return entity
