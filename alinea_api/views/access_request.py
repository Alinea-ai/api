from rest_framework import viewsets, permissions

from alinea_api.models import AccessRequest
from alinea_api.serializers import AccessRequestSerializer


class AccessRequestViewSet(viewsets.ModelViewSet):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(entity=self.request.user.entity)
