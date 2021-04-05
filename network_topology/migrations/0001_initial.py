# Generated by Django 3.1.7 on 2021-04-05 01:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('connected_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network_topology.device')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network_topology.devicetype')),
                ('ip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='network_topology.ip')),
            ],
        ),
    ]
