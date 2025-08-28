from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_requisicion_proveedor_estado_por'),
    ]

    operations = [
        migrations.AddField(
            model_name='salida',
            name='area',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salida',
            name='admision',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

