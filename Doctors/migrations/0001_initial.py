# Generated by Django 4.1.1 on 2023-03-10 01:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorAppointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Appointment', models.DateTimeField(blank=True, null=True)),
                ('Status', models.BooleanField(blank=True, null=True)),
                ('Description', models.CharField(blank=True, max_length=100, null=True)),
                ('Doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Doctor', to=settings.AUTH_USER_MODEL)),
                ('Patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Patient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]