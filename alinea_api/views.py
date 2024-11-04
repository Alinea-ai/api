from rest_framework import viewsets, permissions
from .models import (
    Entity,
    AccessRequest,
    AccessRequestItem,
    UserPersonalInformation,
)
from .serializers import (
    EntitySerializer,
    AccessRequestSerializer,
    AccessRequestItemSerializer,
)

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
