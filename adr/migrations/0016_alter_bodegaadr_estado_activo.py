# Generated by Django 5.0.8 on 2024-12-09 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0015_alter_proyectores_ubicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodegaadr',
            name='estado_activo',
            field=models.CharField(choices=[('', 'Seleccione un estado'), ('Bueno', 'Bueno'), ('Malo', 'Malo'), ('Con Detalles', 'Con Detalles')], default='', max_length=100, verbose_name='Estado Activo'),
        ),
    ]
