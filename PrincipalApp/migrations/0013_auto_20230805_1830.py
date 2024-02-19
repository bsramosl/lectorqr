# Generated by Django 3.2.9 on 2023-08-05 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0012_remove_registro_observacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculomodel',
            name='persona',
        ),
        migrations.AddField(
            model_name='personamodel',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Vehiculo', to='PrincipalApp.vehiculomodel'),
        ),
    ]
