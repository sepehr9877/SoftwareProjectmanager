# Generated by Django 4.1.1 on 2023-03-10 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorappointment',
            name='Status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
