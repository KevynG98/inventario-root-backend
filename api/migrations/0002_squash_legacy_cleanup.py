# Simplified migration to mark legacy cleanup as applied without dropping columns.
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = []
