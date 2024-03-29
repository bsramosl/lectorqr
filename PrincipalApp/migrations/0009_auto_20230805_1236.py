# Generated by Django 3.2.9 on 2023-08-05 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0008_auto_20230805_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personamodel',
            name='tipousuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TipoUsuario', to='PrincipalApp.tipopersonamodel'),
        ),
        migrations.AlterField(
            model_name='vehiculomodel',
            name='persona',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Persona', to=settings.AUTH_USER_MODEL),
        ),
    ]
