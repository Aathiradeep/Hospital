# Generated by Django 5.0.1 on 2024-08-25 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Billing', '0002_remove_billing_billing_date_remove_billing_details_and_more'),
        ('Doctors', '0006_doctor_consultation_fee'),
        ('Patients', '0003_alter_patient_doctor'),
        ('appointments', '0003_appointment_reason_alter_appointment_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_generated', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appointments.appointment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctors.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Patients.patient')),
            ],
        ),
        migrations.DeleteModel(
            name='Billing',
        ),
    ]