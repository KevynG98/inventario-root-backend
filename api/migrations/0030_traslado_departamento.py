from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_salida_area_admision'),
    ]

    operations = [
        migrations.AddField(
            model_name='traslado',
            name='departamento',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]

