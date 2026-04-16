from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salles', '0001_initial'),
        ('produits', '0002_alter_lignevente_options_alter_vente_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AddField(
            model_name='vente',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
