# Generated by Django 5.0.1 on 2024-08-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0003_doctor_working_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='working_hours_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='working_hours_start',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
