# Generated by Django 4.0.1 on 2023-01-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_accepted_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(max_length=10),
        ),
    ]
