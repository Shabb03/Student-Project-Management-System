# Generated by Django 4.0.1 on 2023-01-12 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_status_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='proposal',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='project.proposal'),
            preserve_default=False,
        ),
    ]
