# Generated by Django 4.1.6 on 2023-02-16 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_alter_device_additional_ansible_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='wol',
            field=models.BooleanField(default=False),
        ),
    ]
