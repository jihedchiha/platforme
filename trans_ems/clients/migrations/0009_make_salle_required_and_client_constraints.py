from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_assign_default_salle'),
        ('salles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cin',
            field=models.CharField(max_length=20, unique=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AlterField(
            model_name='abonnement',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AlterField(
            model_name='pack',
            name='salle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together={('cin', 'salle')},
        ),
    ]
