# Generated by Django 4.0.1 on 2023-01-12 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_status_proposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='proposal',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='project.proposal'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='files',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]