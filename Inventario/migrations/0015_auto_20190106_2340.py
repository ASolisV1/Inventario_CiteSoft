# Generated by Django 2.0.2 on 2019-01-06 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0014_auto_20190106_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembro_proyecto',
            name='estado_miembro_proyecto',
            field=models.CharField(choices=[('ACTIVO', 'ACTIVO'), ('INACTIVO', 'INACTIVO')], default='ACTIVO', max_length=50),
        ),
    ]
