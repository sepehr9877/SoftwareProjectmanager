# Generated by Django 4.1.1 on 2023-02-22 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[(1, 'patient'), (2, 'doctor'), (3, 'counselor'), (4, 'manger')], default='patient', max_length=50),
        ),
    ]
