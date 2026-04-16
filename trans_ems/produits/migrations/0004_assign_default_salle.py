from django.db import migrations


def create_default_salle_and_assign(apps, schema_editor):
    Salle = apps.get_model('salles', 'Salle')
    salle, _ = Salle.objects.get_or_create(
        slug='salle-principale',
        defaults={
            'nom': 'Salle Principale',
            'pack_saas': 'starter',
            'actif': True,
        }
    )

    Produit = apps.get_model('produits', 'Produit')
    Vente = apps.get_model('produits', 'Vente')

    Produit.objects.filter(salle__isnull=True).update(salle_id=salle.id)
    Vente.objects.filter(salle__isnull=True).update(salle_id=salle.id)


def reverse(apps, schema_editor):
    Salle = apps.get_model('salles', 'Salle')
    salle = Salle.objects.filter(slug='salle-principale').first()
    if not salle:
        return

    Produit = apps.get_model('produits', 'Produit')
    Vente = apps.get_model('produits', 'Vente')

    Produit.objects.filter(salle_id=salle.id).update(salle=None)
    Vente.objects.filter(salle_id=salle.id).update(salle=None)


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0003_add_salle_nullable'),
        ('salles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_salle_and_assign, reverse),
    ]
