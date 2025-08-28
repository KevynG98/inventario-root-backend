from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_add_user_fields_entrada_salida'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisicion',
            name='usuario',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]

