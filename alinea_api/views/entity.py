from rest_framework import viewsets, permissions

from alinea_api.models import Entity
from alinea_api.serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [permissions.IsAuthenticated]