from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salles', '0001_initial'),
        ('seances', '0006_alter_reservation_taille_gilet_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='seance',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
