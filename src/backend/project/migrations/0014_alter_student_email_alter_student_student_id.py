# Generated by Django 4.0.1 on 2023-01-20 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_alter_professor_email_alter_student_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
