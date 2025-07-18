# Generated by Django 5.0.8 on 2024-11-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0008_remove_reporteaccesorios_accesorio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinone',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='allinoneadmins',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='azotea',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='bodegaadr',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='minipc',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='proyectores',
            name='creado_por',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registrador por'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='operador_entrega',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Operador que entrega'),
        ),
        migrations.AlterField(
            model_name='reporte',
            name='reporte_creado',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Recepcionado por'),
        ),
    ]
