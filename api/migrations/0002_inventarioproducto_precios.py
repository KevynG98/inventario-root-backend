from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventarioproducto',
            name='precio_compre',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='inventarioproducto',
            name='precio_stock',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
