# Generated by Django 5.0.8 on 2024-10-22 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0003_alter_allinone_bdo_alter_allinoneadmins_bdo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyectores',
            name='sala',
        ),
    ]
