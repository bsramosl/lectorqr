# Generated by Django 3.2.9 on 2023-07-15 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0005_auto_20230701_2109'),
    ]

    operations = [
        migrations.AddField(
            model_name='registro',
            name='observacion',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]