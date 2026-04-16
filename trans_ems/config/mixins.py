class TenantMixin:
    """
    Mixin à ajouter aux APIViews pour faciliter le filtrage par salle.
    Utilise 'request.salle_id' défini par le TenantMiddleware.
    """

    def get_tenant_queryset(self, model_class):
        """
        Retourne un QuerySet filtré par la salle active.
        Si salle_id est None (SuperAdmin global), retourne tout.
        """
        queryset = model_class.objects.all()
        
        # Le middleware a déjà fait le travail d'identification
        salle_id = getattr(self.request, 'salle_id', None)

        if salle_id:
            # On filtre si une salle spécifique est demandée ou imposée
            return queryset.filter(salle_id=salle_id)
        
        return queryset

    def set_tenant_salle(self, data):
        """
        Injecte automatiquement la salle active dans les données (ex: pour un POST).
        """
        salle_id = getattr(self.request, 'salle_id', None)
        if salle_id:
            data['salle'] = salle_id
        return data
