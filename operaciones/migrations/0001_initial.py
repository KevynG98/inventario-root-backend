from django.db import migrations, models
import operaciones.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Operacion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField()),
                ("dia", models.CharField(max_length=20)),
                ("hora", models.CharField(max_length=20)),
                ("paciente", models.CharField(max_length=255)),
                ("edad", models.PositiveIntegerField()),
                ("especialidad", models.CharField(max_length=100)),
                ("procedimiento", models.TextField()),
                ("cirujano1", models.CharField(max_length=255)),
                ("cirujano2", models.CharField(blank=True, max_length=255, null=True)),
                ("cirujano3", models.CharField(blank=True, max_length=255, null=True)),
                ("anestesiologo", models.CharField(blank=True, max_length=255, null=True)),
                ("pediatra", models.CharField(blank=True, max_length=255, null=True)),
                ("seguro", models.CharField(max_length=255)),
                ("material", models.TextField(blank=True, null=True)),
                ("comentarios", models.TextField(blank=True, null=True)),
                ("estatus", models.CharField(choices=[("Programado", "Programado"), ("En Proceso", "En Proceso"), ("En Recuperación", "En Recuperación"), ("Finalizado", "Finalizado"), ("Cancelada", "Cancelada")], default="Programado", max_length=20)),
                ("historial", models.JSONField(blank=True, default=operaciones.models.default_historial)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Operación",
                "verbose_name_plural": "Operaciones",
                "ordering": ("-fecha", "hora"),
            },
        ),
    ]
