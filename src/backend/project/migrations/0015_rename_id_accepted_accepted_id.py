# Generated by Django 4.0.1 on 2023-01-21 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0014_alter_student_email_alter_student_student_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accepted',
            old_name='id',
            new_name='accepted_id',
        ),
    ]
