# Generated by Django 2.0.5 on 2018-07-24 20:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0003_auto_20180724_0334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso_proyecto',
            name='fecha_recurso_proyecto',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
