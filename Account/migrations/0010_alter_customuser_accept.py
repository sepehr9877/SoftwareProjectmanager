# Generated by Django 4.1.1 on 2023-03-31 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0009_customuser_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='accept',
            field=models.BooleanField(default=False),
        ),
    ]
