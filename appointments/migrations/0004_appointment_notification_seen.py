# Generated by Django 5.0.1 on 2024-08-25 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_appointment_reason_alter_appointment_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='notification_seen',
            field=models.BooleanField(default=False),
        ),
    ]
