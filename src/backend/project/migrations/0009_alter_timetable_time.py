# Generated by Django 4.0.1 on 2023-01-13 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_meeting_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='time',
            field=models.CharField(choices=[('0', 'Not Available'), ('1', '09:00-10:00'), ('2', '10:00-11:00'), ('3', '11:00-12:00'), ('4', '12:00-13:00'), ('5', '14:00-15:00'), ('6', '15:00-16:00'), ('7', '16:00-16:00'), ('8', '17:00-18:00')], default='1', max_length=20),
        ),
    ]
