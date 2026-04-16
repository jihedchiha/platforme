from django.core.management.base import BaseCommand
from users.models import Utilisateur

class Command(BaseCommand):
    help = "Crée ou promeut un utilisateur au rôle de SuperAdmin (Gestion de la plateforme)"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Nom d\'utilisateur', required=True)
        parser.add_argument('--email', type=str, help='Email de l\'utilisateur')
        parser.add_argument('--password', type=str, help='Mot de passe de l\'utilisateur')

    def handle(self, *args, **options):
        username = options['username']
        email = options.get('email')
        password = options.get('password')

        user, created = Utilisateur.objects.get_or_create(username=username)
        
        if created:
            if not password:
                self.stdout.write(self.style.ERROR("Un mot de passe est requis pour la création d'un nouvel utilisateur."))
                return
            user.email = email or ''
            user.set_password(password)
            self.stdout.write(self.style.SUCCESS(f"Utilisateur '{username}' créé."))
        else:
            self.stdout.write(self.style.WARNING(f"Utilisateur '{username}' déjà existant. Promotion en cours..."))

        user.role = 'superadmin'
        user.is_staff = True
        user.is_superuser = True
        user.save()

        self.stdout.write(self.style.SUCCESS(f"🚀 Succès : '{username}' est maintenant un SuperAdmin de la plateforme."))
