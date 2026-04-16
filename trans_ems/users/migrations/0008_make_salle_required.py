from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_assign_default_salle'),
        ('salles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
