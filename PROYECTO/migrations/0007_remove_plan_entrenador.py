# Generated by Django 3.2 on 2024-12-25 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PROYECTO', '0006_auto_20241225_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='entrenador',
        ),
    ]
