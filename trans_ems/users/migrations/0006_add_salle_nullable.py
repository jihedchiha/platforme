from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salles', '0001_initial'),
        ('users', '0005_alter_utilisateur_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
