from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_admisionmedicotratante_antecedenteclinico_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvolucionClinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resumen', models.CharField(blank=True, max_length=255, null=True)),
                ('contenido', models.TextField()),
                ('medico_nombre', models.CharField(blank=True, max_length=255, null=True)),
                ('medico_colegiado', models.CharField(blank=True, max_length=100, null=True)),
                ('creado_por_username', models.CharField(blank=True, max_length=150, null=True)),
                ('actualizado_por_username', models.CharField(blank=True, max_length=150, null=True)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
                ('admision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evoluciones_clinicas', to='api.admision')),
            ],
            options={
                'verbose_name': 'Evolución clínica',
                'verbose_name_plural': 'Evoluciones clínicas',
                'ordering': ('-creado_en',),
            },
        ),
    ]
