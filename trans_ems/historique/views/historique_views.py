from rest_framework.views import APIView
from config.mixins        import TenantMixin
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta

from drf_spectacular.utils import extend_schema, OpenApiParameter

from users.permissions import IsAdminOrPersonnel
from historique.serializers import HistoriqueSerializer
from historique.services import HistoriqueService
from historique.models import Historique   # ← nécessaire pour get_tenant_queryset


class HistoriqueListView(TenantMixin, APIView):
    permission_classes = [IsAdminOrPersonnel]

    @extend_schema(
        summary="Historique des actions",
        description="Retourne l'historique (7 derniers jours par défaut) avec filtres possibles.",
        parameters=[
            OpenApiParameter(name='date', type=str, description='YYYY-MM-DD', required=False),
            OpenApiParameter(name='date_debut', type=str, description='YYYY-MM-DD', required=False),
            OpenApiParameter(name='date_fin', type=str, description='YYYY-MM-DD', required=False),
        ],
        responses={200: HistoriqueSerializer(many=True)}
    )
    def get(self, request):

        date_param = request.query_params.get('date')
        date_debut_param = request.query_params.get('date_debut')
        date_fin_param = request.query_params.get('date_fin')

        try:
            # 1. Filtre par date exacte + salle
            if date_param:
                date_filtre  = date.fromisoformat(date_param)
                historiques  = self.get_tenant_queryset(Historique).select_related('personnel').filter(
                    created_at__date=date_filtre
                )

            # 2. Filtre par intervalle + salle
            elif date_debut_param and date_fin_param:
                date_debut   = date.fromisoformat(date_debut_param)
                date_fin     = date.fromisoformat(date_fin_param)
                historiques  = self.get_tenant_queryset(Historique).select_related('personnel').filter(
                    created_at__date__gte=date_debut,
                    created_at__date__lte=date_fin
                )

            # 3. Par défaut → 7 derniers jours + salle
            else:
                date_fin     = date.today()
                date_debut   = date_fin - timedelta(days=7)
                historiques  = self.get_tenant_queryset(Historique).select_related('personnel').filter(
                    created_at__date__gte=date_debut,
                    created_at__date__lte=date_fin
                )

        except ValueError:
            return Response(
                {'error': 'Format date invalide. Utilisez YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HistoriqueSerializer(historiques, many=True)
        return Response(serializer.data)