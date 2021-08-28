# Generated by Django 3.2.6 on 2021-08-28 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectionMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Connection Method',
                'verbose_name_plural': 'Connection Methods',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hostname', models.CharField(max_length=255)),
                ('mac_address', models.CharField(blank=True, max_length=17, null=True)),
                ('description', models.CharField(max_length=500)),
                ('snmp_enabled', models.BooleanField(default=False)),
                ('subdomain', models.CharField(blank=True, max_length=50, null=True)),
                ('connected_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network_topology.device')),
                ('connection_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network_topology.connectionmethod')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Device Category',
                'verbose_name_plural': 'Device Categories',
            },
        ),
        migrations.CreateModel(
            name='DNSProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('use_api', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'DNS Provider',
                'verbose_name_plural': 'DNS Providers',
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unique=True)),
            ],
            options={
                'verbose_name': 'IP',
                'verbose_name_plural': 'IPs',
            },
        ),
        migrations.CreateModel(
            name='MonitoringGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('group_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Monitoring Group',
                'verbose_name_plural': 'Monitoring Groups',
            },
        ),
        migrations.CreateModel(
            name='MonitoringTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('template_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Monitoring Template',
                'verbose_name_plural': 'Monitoring Templates',
            },
        ),
        migrations.CreateModel(
            name='Registrar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('use_api', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1000)),
                ('https', models.BooleanField(default=False)),
                ('use_ip', models.BooleanField(default=False)),
                ('path', models.CharField(blank=True, max_length=255, null=True)),
                ('hosted_on', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network_topology.device')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dns_provider', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='network_topology.dnsprovider')),
                ('registrar', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='network_topology.registrar')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='network_topology.devicecategory')),
                ('monitoring_templates', models.ManyToManyField(blank=True, to='network_topology.MonitoringTemplate')),
            ],
            options={
                'verbose_name': 'Device Type',
                'verbose_name_plural': 'Device Types',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network_topology.devicetype'),
        ),
        migrations.AddField(
            model_name='device',
            name='domain',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='network_topology.domain'),
        ),
        migrations.AddField(
            model_name='device',
            name='ip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='network_topology.ip'),
        ),
        migrations.AddField(
            model_name='device',
            name='monitoring_groups',
            field=models.ManyToManyField(to='network_topology.MonitoringGroup'),
        ),
        migrations.AddField(
            model_name='device',
            name='monitoring_templates',
            field=models.ManyToManyField(blank=True, to='network_topology.MonitoringTemplate'),
        ),
    ]
