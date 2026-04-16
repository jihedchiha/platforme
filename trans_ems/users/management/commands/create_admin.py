from django.core.management.base import BaseCommand
from users.models import Utilisateur

class Command(BaseCommand):
    help = "Crée un Administrateur de Studio (Gestion locale)"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Nom d\'utilisateur', required=True)
        parser.add_argument('--email', type=str, help='Email de l\'utilisateur', required=True)
        parser.add_argument('--password', type=str, help='Mot de passe de l\'utilisateur', required=True)

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if Utilisateur.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"L'utilisateur '{username}' existe déjà."))
            return

        user = Utilisateur.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin'
        )
        
        user.is_staff = True # Permet l'accès au panel si besoin
        user.save()

        self.stdout.write(self.style.SUCCESS(f"✅ Succès : Administrateur studio '{username}' créé avec succès."))
