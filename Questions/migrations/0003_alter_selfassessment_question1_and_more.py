# Generated by Django 4.1.1 on 2023-03-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Questions', '0002_alter_selfassessment_question9'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfassessment',
            name='Question1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question2',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question3',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question4',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question5',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question6',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question7',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question8',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='selfassessment',
            name='Question9',
            field=models.CharField(max_length=50),
        ),
    ]