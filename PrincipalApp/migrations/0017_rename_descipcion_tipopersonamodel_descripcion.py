# Generated by Django 3.2.9 on 2023-08-09 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0016_auto_20230805_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tipopersonamodel',
            old_name='descipcion',
            new_name='descripcion',
        ),
    ]
