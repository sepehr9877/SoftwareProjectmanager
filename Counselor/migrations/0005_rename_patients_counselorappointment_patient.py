# Generated by Django 4.1.1 on 2023-03-10 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Counselor', '0004_counselorappointment_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='counselorappointment',
            old_name='Patients',
            new_name='Patient',
        ),
    ]
