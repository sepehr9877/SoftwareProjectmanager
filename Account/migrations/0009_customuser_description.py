# Generated by Django 4.1.1 on 2023-03-31 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0008_customuser_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.CharField(default='Pending', max_length=100),
        ),
    ]
