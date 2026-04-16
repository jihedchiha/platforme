from clients.models import Client
from seances.models import Reservation
from django.db.models import Q


class ClientService:

    @staticmethod
    def creer_client(data):
        salle_id = data.get('salle')
        if not salle_id:
            raise ValueError("La salle est obligatoire pour créer un client")

        # Vérification CIN unique AU SEIN de la salle
        if Client.objects.filter(cin=data['cin'], salle_id=salle_id).exists():
            raise ValueError("Un client avec ce CIN existe déjà dans cette salle")

        client = Client.objects.create(
            nom            = data['nom'],
            prenom         = data['prenom'],
            cin            = data['cin'],
            telephone_1    = data['telephone_1'],
            telephone_2    = data.get('telephone_2', ''),
            email          = data.get('email', ''),
            date_naissance = data.get('date_naissance', None),
            photo          = data.get('photo', None),
            salle_id       = salle_id,  # ← Ajout de la salle
        )
        
        return client

    @staticmethod
    
    def modifier_client(client, data):

    # 🔹 Vérification CIN unique
        nouveau_cin = data.get('cin')
        if nouveau_cin and nouveau_cin != client.cin:
            if Client.objects.filter(cin=nouveau_cin, salle=client.salle).exists():
                raise ValueError("Un client avec ce CIN existe déjà dans cette salle")

    # 🔹 Champs modifiables
        champs = [
            'nom', 'prenom', 'cin',
            'telephone_1', 'telephone_2',
            'email', 'date_naissance', 'photo'
        ]

        for champ in champs:
            if champ in data:
                value = data[champ]

            # 🔥 IMPORTANT : gérer FormData (QueryDict → liste)
                if isinstance(value, list):
                    value = value[0]

            # 🔥 Nettoyage valeur vide
                if isinstance(value, str):
                    value = value.strip()

            # 🔥 SUPPRESSION telephone_2
                if champ == 'telephone_2' and value == '':
                    value = None  # ou '' selon ton modèle

            # 🔥 Validation téléphone 1 (obligatoire)
                if champ == 'telephone_1':
                    if not value or not value.isdigit() or len(value) != 8:
                       raise ValueError("Téléphone 1 invalide (8 chiffres obligatoires)")

            # 🔥 Validation téléphone 2 (optionnel)
                if champ == 'telephone_2' and value:
                   if not value.isdigit() or len(value) != 8:
                      raise ValueError("Téléphone 2 invalide (8 chiffres)")

            # 🔥 Email vide → null
                if champ == 'email' and value == '':
                   value = None

                setattr(client, champ, value)

        client.save()
        return client

    @staticmethod
    def rechercher_clients(query):
        return Client.objects.filter(
            Q(cin__icontains=query)         |
            Q(nom__icontains=query)         |
            Q(prenom__icontains=query)      |
            Q(telephone_1__icontains=query)
        )


    @staticmethod
    def supprimer_client(client):

        # récupérer les réservations actives
        reservations = Reservation.objects.filter(
            abonnement__client=client,
            statut__in=['en_attente', 'present']
        ).select_related('seance')

        # libérer les places
        for r in reservations:
            seance = r.seance
            seance.places_disponibles += 1
            seance.save()

        # supprimer le client (cascade auto)
        client.delete()