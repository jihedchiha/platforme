from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from users.permissions import IsSuperAdmin
from ..models import Salle
from ..serializers import SalleSerializer
from ..services.salle_service import SalleService

class SalleViewSet(viewsets.ModelViewSet):
    """
    CRUD des salles - Réservé au SuperAdmin
    """
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    permission_classes = [IsSuperAdmin]

    @action(detail=False, methods=['get'], permission_classes=[])
    def config(self, request):
        """
        Endpoint pour récupérer la config de branding
        """
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return Response({'error': 'En-tête X-Tenant-ID manquant'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            config = SalleService.get_config(tenant_id)
            return Response(config)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
