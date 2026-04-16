from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seances', '0008_assign_default_salle'),
        ('salles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seance',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
