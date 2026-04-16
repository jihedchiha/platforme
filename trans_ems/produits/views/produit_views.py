from rest_framework.views    import APIView
from config.mixins           import TenantMixin
from rest_framework.response import Response
from rest_framework          import status

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from users.permissions              import IsAdmin, IsAdminOrPersonnel
from produits.serializers           import ProduitSerializer, CreerProduitSerializer, ModifierProduitSerializer
from produits.services              import ProduitService


class ProduitListView(TenantMixin, APIView):

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [IsAdminOrPersonnel()]

    @extend_schema(
        summary   = 'Liste des produits',
        responses = {200: ProduitSerializer(many=True)}
    )
    def get(self, request):
        # Filtrage des produits actifs par salle
        produits   = self.get_tenant_queryset(Produit).filter(est_actif=True)
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary   = 'Créer un produit',
        request   = CreerProduitSerializer,
        responses = {
            201: ProduitSerializer,
            400: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
        # Injecter la salle active avant validation
        data = self.set_tenant_salle(request.data.copy())
        serializer = CreerProduitSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        produit    = ProduitService.creer(serializer.validated_data)
        return Response(
            ProduitSerializer(produit).data,
            status=status.HTTP_201_CREATED
        )


class ProduitDetailView(TenantMixin, APIView):

    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdmin()]
        return [IsAdminOrPersonnel()]

    @extend_schema(
        summary   = 'Modifier un produit',
        request   = ModifierProduitSerializer,
        responses = {
            200: ProduitSerializer,
            400: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        }
    )
    def put(self, request, produit_id):
        serializer = ModifierProduitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérification que le produit appartient à la salle active
        try:
            produit = self.get_tenant_queryset(Produit).get(id=produit_id)
        except Produit.DoesNotExist:
            return Response({'error': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)

        resultat = ProduitService.modifier(produit_id, serializer.validated_data)

        if isinstance(resultat, dict) and 'error' in resultat:
            return Response(
                resultat,
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(ProduitSerializer(resultat).data)