from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Utilisateur


class AuthService:

    @staticmethod
    def login(username, password):
        try:
            user = Utilisateur.objects.get(username=username) # Utilisation de .get() standard
        except Utilisateur.DoesNotExist:
            raise ValueError("Nom d'utilisateur incorrect")

        if not user.check_password(password):
            raise ValueError("Mot de passe incorrect")

        if not user.is_active:
            raise ValueError("Ce compte est désactivé")

        refresh = RefreshToken.for_user(user)

        return {
            'access' : str(refresh.access_token),
            'refresh': str(refresh),
            'user'   : {
                'id'    : str(user.id),
                'role'  : user.role,
                'nom'   : user.get_full_name(),
                'salles': AuthService.get_user_salles_data(user),  # ← Utilisation du helper
            },
            'instance': user
        }

    @staticmethod
    def get_user_salles_data(user):
        """Helper pour formater les salles autorisées pour un utilisateur."""
        salles_data = []

        # 1. PERSONNEL : Salle unique
        if user.role == 'personnel' and user.salle:
            salles_data.append({
                'id': str(user.salle.id),
                'nom': user.salle.nom,
                'logo': user.salle.logo.url if user.salle.logo else None,
                'couleur': user.salle.couleur_primaire
            })

        # 2. FOURNISSEUR : Salles liées
        elif hasattr(user, 'fournisseur'):
            salle_links = user.fournisseur.salles.filter(statut='actif').select_related('salle')
            for link in salle_links:
                salles_data.append({
                    'id': str(link.salle.id),
                    'nom': link.salle.nom,
                    'logo': link.salle.logo.url if link.salle.logo else None,
                    'couleur': link.salle.couleur_primaire
                })

        # 3. ADMIN : Toutes les salles
        elif user.role == 'admin':
            from salles.models import Salle
            all_salles = Salle.objects.filter(actif=True)
            for s in all_salles:
                salles_data.append({
                    'id': str(s.id),
                    'nom': s.nom,
                    'logo': s.logo.url if s.logo else None,
                    'couleur': s.couleur_primaire
                })

        return salles_data
    @staticmethod
    def change_password(user, old_password, new_password):

        if not user.check_password(old_password):
            raise ValueError("Ancien mot de passe incorrect")

        user.set_password(new_password)
        user.save()

        return True

    @staticmethod
    def creer_personnel(data):
        if Utilisateur.objects.filter(cin=data['cin']).exists():
            raise ValueError("Ce CIN existe déjà")

        if Utilisateur.objects.filter(username=data['username']).exists():
            raise ValueError("Ce nom d'utilisateur existe déjà")

        user = Utilisateur.objects.create_user(
            username      = data['username'],
            password      = data['password'],
            first_name    = data['first_name'],
            last_name     = data['last_name'],
            email         = data['email'],   # ← ajouter
            cin           = data['cin'],
            telephone     = data.get('telephone', ''),
            role          = 'personnel',
            shift         = data['shift'],
            date_embauche = data['date_embauche'],
        )

        return user