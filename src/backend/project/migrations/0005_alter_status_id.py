# Generated by Django 4.0.1 on 2023-01-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_alter_status_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
