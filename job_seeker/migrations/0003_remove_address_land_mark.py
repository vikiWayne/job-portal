# Generated by Django 3.0.4 on 2020-04-15 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0002_jobseeker_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='land_mark',
        ),
    ]
