# Generated by Django 3.0.4 on 2020-04-19 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0004_auto_20200416_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumes',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes'),
        ),
    ]