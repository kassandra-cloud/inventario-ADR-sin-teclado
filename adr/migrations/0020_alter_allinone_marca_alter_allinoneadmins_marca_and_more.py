# Generated by Django 5.0.8 on 2025-01-23 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adr', '0019_alter_azotea_estado_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinone',
            name='marca',
            field=models.CharField(choices=[('', 'Seleccione una marca'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Apple', 'Apple'), ('Asus', 'Asus')], default='', max_length=100, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='allinoneadmins',
            name='marca',
            field=models.CharField(choices=[('', 'Seleccione una marca'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Apple', 'Apple'), ('Asus', 'Asus')], default='', max_length=100, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='azotea',
            name='marca',
            field=models.CharField(choices=[('', 'Seleccione una marca'), ('A0LFCL', 'A0LFCL'), ('Apple', 'Apple'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Dell', 'Dell'), ('Asus', 'Asus')], default='', max_length=100, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='bodegaadr',
            name='marca',
            field=models.CharField(choices=[('', 'Seleccione una marca'), ('Apple', 'Apple'), ('Epson', 'Epson'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Panasonic', 'Panasonic'), ('Viewsonic', 'Viewsonic'), ('Asus', 'Asus')], default='', max_length=100, verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='notebook',
            name='marca',
            field=models.CharField(choices=[('', 'Seleccione una marca'), ('Dell', 'Dell'), ('HP', 'HP'), ('Lenovo', 'Lenovo'), ('Asus', 'Asus')], default='', max_length=100, verbose_name='Marca'),
        ),
    ]
