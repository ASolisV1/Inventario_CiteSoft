# Generated by Django 2.0 on 2018-08-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0009_auto_20180804_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='recursos',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')], default='ACTIVO', max_length=10),
        ),
    ]