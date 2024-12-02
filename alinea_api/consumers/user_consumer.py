from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json


from alinea_api.models import Entity, CustomUser


class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = await self.get_dummy_user()

        if user_id:
            self.group_name = f'user_{user_id.id}_group'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            await self.send(text_data=json.dumps({'message': f'Connected to {self.group_name}'}))
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def access_request_event(self, event):
        message = event['message']
        await self.send(text_data=message)

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
