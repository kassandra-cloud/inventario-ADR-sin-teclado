# Generated by Django 5.0.2 on 2025-06-12 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0023_remove_monitor_pulgadas_monitor_asignado_a_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='tipo_audio',
        ),
        migrations.RemoveField(
            model_name='monitor',
            name='pulgadas',
        ),
        migrations.AddField(
            model_name='monitor',
            name='asignado_a',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Asignado a'),
        ),
        migrations.AlterField(
            model_name='monitor',
            name='marca',
            field=models.CharField(default='', max_length=100, verbose_name='Marca'),
        ),
    ]
