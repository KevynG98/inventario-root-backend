from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_requisicion_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='proveedor',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='requisicion',
            name='estado_actualizado_por',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]

