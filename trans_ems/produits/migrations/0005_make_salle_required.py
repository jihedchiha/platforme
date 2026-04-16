from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0004_assign_default_salle'),
        ('salles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AlterField(
            model_name='vente',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
