# Generated by Django 5.0.1 on 2024-08-24 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0004_doctor_working_hours_end_doctor_working_hours_start'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='working_hours',
        ),
    ]