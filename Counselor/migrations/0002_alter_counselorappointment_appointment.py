# Generated by Django 4.1.1 on 2023-02-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Counselor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counselorappointment',
            name='Appointment',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
