# Generated by Django 3.0.4 on 2020-04-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0003_remove_address_land_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='profile_picture',
            field=models.ImageField(blank=True, default='employee.png', null=True, upload_to='employees'),
        ),
    ]