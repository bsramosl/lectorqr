# Generated by Django 3.2.9 on 2023-08-05 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0013_auto_20230805_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personamodel',
            name='vehiculo',
        ),
        migrations.AddField(
            model_name='vehiculomodel',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Persona', to=settings.AUTH_USER_MODEL),
        ),
    ]