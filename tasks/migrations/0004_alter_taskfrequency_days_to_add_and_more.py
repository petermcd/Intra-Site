# Generated by Django 4.0.3 on 2022-08-04 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_taskfrequency_task_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskfrequency',
            name='days_to_add',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='taskfrequency',
            name='months_to_add',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='taskfrequency',
            name='years_to_add',
            field=models.IntegerField(default=0),
        ),
    ]
