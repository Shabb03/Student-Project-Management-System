# Generated by Django 4.0.1 on 2023-01-17 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_alter_timetable_time_alter_timetable_venue'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted',
            name='message',
            field=models.TextField(default='No Reason Provided'),
        ),
    ]
