from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salles', '0001_initial'),
        ('historique', '0002_rename_utilisateur_historique_personnel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historique',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
