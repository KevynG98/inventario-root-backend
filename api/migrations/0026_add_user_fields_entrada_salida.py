from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_traslado_trasladoitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='aplicado_por',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='aplicado_por',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

