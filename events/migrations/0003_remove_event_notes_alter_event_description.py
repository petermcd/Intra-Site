# Generated by Django 4.0.3 on 2022-04-15 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_accommodation_options_alter_event_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='notes',
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=1000),
        ),
    ]
