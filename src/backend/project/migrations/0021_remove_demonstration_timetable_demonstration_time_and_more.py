# Generated by Django 4.0.1 on 2023-02-06 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_alter_status_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demonstration',
            name='timetable',
        ),
        migrations.AddField(
            model_name='demonstration',
            name='time',
            field=models.CharField(choices=[('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00')], default='09:00', max_length=20),
        ),
        migrations.AddField(
            model_name='demonstration',
            name='venue',
            field=models.CharField(choices=[('Q-Business School', 'Q-Business School'), ('H-Exwell Medical', 'H-Exwell Medical'), ('C-Henry Grattan', 'C-Henry Grattan'), ('T-Larkin Theatre', 'T-Larkin Theatre'), ('X-Londsdale', 'X-Londsdale'), ('S-Stokes', 'S-Stokes'), ('L-McNulty', 'L-McNulty')], default='Q-Business School', max_length=20),
        ),
    ]
