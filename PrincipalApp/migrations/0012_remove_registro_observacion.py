# Generated by Django 3.2.9 on 2023-08-05 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PrincipalApp', '0011_auto_20230805_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registro',
            name='observacion',
        ),
    ]
