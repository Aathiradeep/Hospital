# Generated by Django 5.0.1 on 2024-08-28 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0003_alter_patient_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
