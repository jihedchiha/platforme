from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salles', '0001_initial'),
        ('clients', '0006_pack_remove_abonnement_type_alter_client_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AddField(
            model_name='abonnement',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
        migrations.AddField(
            model_name='pack',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salles.salle'),
        ),
    ]
