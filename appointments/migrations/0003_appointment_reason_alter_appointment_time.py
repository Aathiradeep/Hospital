# Generated by Django 5.0.1 on 2024-08-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_remove_appointment_notes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(),
        ),
    ]
