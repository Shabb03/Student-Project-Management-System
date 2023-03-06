# Generated by Django 4.0.1 on 2023-02-19 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0034_alter_accepted_proposal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('proposal', models.DateField(null=True)),
                ('srs', models.DateField(null=True)),
                ('documentation', models.DateField(null=True)),
                ('assesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('demoItem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.demonstrationitem')),
            ],
        ),
    ]
