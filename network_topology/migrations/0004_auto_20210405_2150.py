# Generated by Django 3.1.7 on 2021-04-05 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network_topology', '0003_device_mac_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='mac_address',
            field=models.CharField(max_length=17),
        ),
    ]
