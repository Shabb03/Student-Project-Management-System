# Generated by Django 4.0.1 on 2023-02-19 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0035_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deadline',
            name='assesor',
        ),
        migrations.RemoveField(
            model_name='deadline',
            name='demoItem',
        ),
    ]
