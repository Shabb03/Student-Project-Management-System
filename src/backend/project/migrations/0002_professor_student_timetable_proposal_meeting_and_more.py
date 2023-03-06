# Generated by Django 4.0.1 on 2023-01-11 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('student_id', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.CharField(choices=[('0', 'Not Available'), ('1', '09:00-10:00'), ('2', '10:00-11:00'), ('3', '11:00-12:00'), ('4', '12:00-13:00'), ('5', '14:00-15:00'), ('6', '15:00-16:00'), ('7', '16:00-16:00'), ('8', '17:00-18:00')], default='0', max_length=20)),
                ('venue', models.CharField(choices=[('Q', 'Q-Business School'), ('H', 'H-Exwell Medical'), ('C', 'C-Henry Grattan'), ('T', 'T-Larkin Theatre'), ('X', 'X-Londsdale'), ('S', 'S-Stokes'), ('L', 'L-McNulty')], default='Q', max_length=20)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('staff', models.CharField(max_length=50)),
                ('time', models.DateTimeField(auto_now=True)),
                ('introduction', models.TextField(default='')),
                ('outline', models.TextField(default='')),
                ('background', models.TextField(default='')),
                ('goals', models.TextField(default='')),
                ('tools', models.TextField(default='')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('accepted', models.BooleanField(default=False)),
                ('tostudent', models.BooleanField(default=False)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Demonstration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
                ('timetable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.timetable')),
            ],
        ),
        migrations.CreateModel(
            name='Accepted',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accepted', models.BooleanField(default=False)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.proposal')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='project.proposal')),
                ('submitted', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('srs', models.BooleanField(default=False)),
                ('documentation', models.BooleanField(default=False)),
                ('mark', models.BooleanField(default=False)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Marking',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='project.proposal')),
                ('time', models.DateTimeField(auto_now=True)),
                ('submitted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('srs_report', models.TextField(default='')),
                ('srs_mark', models.IntegerField(default=0)),
                ('design_report', models.TextField(default='')),
                ('design_mark', models.IntegerField(default=0)),
                ('implementation_report', models.TextField(default='')),
                ('implementation_mark', models.IntegerField(default=0)),
                ('testing_report', models.TextField(default='')),
                ('testing_mark', models.IntegerField(default=0)),
                ('documentation_report', models.TextField(default='')),
                ('documentation_mark', models.IntegerField(default=0)),
                ('demonstration_report', models.TextField(default='')),
                ('demonstration_mark', models.IntegerField(default=0)),
                ('video_report', models.TextField(default='')),
                ('video_mark', models.IntegerField(default=0)),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.professor')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='project.proposal')),
                ('srs', models.FileField(blank=True, upload_to='media/srs')),
                ('documentation', models.FileField(blank=True, upload_to='media/docs')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.student')),
            ],
        ),
    ]