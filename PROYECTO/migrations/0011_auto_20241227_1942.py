# Generated by Django 3.2 on 2024-12-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PROYECTO', '0010_auto_20241227_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carritoitem',
            name='usuario',
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.PositiveIntegerField(),
        ),
    ]