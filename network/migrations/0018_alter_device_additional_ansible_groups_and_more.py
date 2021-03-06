# Generated by Django 4.0.3 on 2022-05-12 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_alter_device_applications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='additional_ansible_groups',
            field=models.ManyToManyField(blank=True, null=True, to='network.additionalansiblegroup'),
        ),
        migrations.AlterField(
            model_name='device',
            name='applications',
            field=models.ManyToManyField(blank=True, null=True, to='network.application'),
        ),
    ]
