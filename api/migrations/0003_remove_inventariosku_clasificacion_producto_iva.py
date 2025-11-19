from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_squash_legacy_cleanup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventariosku',
            name='clasificacion_producto',
        ),
        migrations.RemoveField(
            model_name='inventariosku',
            name='iva',
        ),
    ]
