# Generated by Django 4.0.3 on 2022-04-15 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_application_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='ansible_managed',
            field=models.BooleanField(default=True),
        ),
    ]