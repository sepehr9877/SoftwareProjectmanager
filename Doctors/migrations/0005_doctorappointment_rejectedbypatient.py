# Generated by Django 4.1.1 on 2023-04-05 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0004_rename_status_doctorappointment_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorappointment',
            name='RejectedByPatient',
            field=models.BooleanField(default=False),
        ),
    ]