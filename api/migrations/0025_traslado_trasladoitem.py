from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_inventariosku_clasificacion_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traslado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bodega_origen', models.CharField(max_length=100)),
                ('bodega_destino', models.CharField(max_length=100)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('enviado_por', models.CharField(blank=True, max_length=150, null=True)),
                ('entregamos_a', models.CharField(blank=True, max_length=150, null=True)),
                ('recibido_por', models.CharField(blank=True, max_length=150, null=True)),
                ('estatus', models.CharField(choices=[('ENVIADO', 'Enviado'), ('RECIBIDO', 'Recibido'), ('ANULADO', 'Anulado')], default='ENVIADO', max_length=10)),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
                ('fecha_recibido', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrasladoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('cantidad', models.PositiveIntegerField()),
                ('traslado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.traslado')),
            ],
        ),
    ]

