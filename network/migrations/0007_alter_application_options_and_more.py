# Generated by Django 4.0.3 on 2022-04-14 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_devicetype_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': 'Application', 'verbose_name_plural': 'Applications'},
        ),
        migrations.AlterModelOptions(
            name='connectiontype',
            options={'verbose_name': 'Connection type', 'verbose_name_plural': 'Connection types'},
        ),
        migrations.AlterModelOptions(
            name='device',
            options={'verbose_name': 'Device', 'verbose_name_plural': 'Devices'},
        ),
        migrations.AlterModelOptions(
            name='devicetype',
            options={'verbose_name': 'Device type', 'verbose_name_plural': 'Device types'},
        ),
        migrations.AlterModelOptions(
            name='domainname',
            options={'verbose_name': 'Domain name', 'verbose_name_plural': 'Domain names'},
        ),
        migrations.AlterModelOptions(
            name='model',
            options={'verbose_name': 'Model', 'verbose_name_plural': 'Models'},
        ),
        migrations.AlterModelOptions(
            name='operatingsystem',
            options={'verbose_name': 'Operating system', 'verbose_name_plural': 'Operating systems'},
        ),
        migrations.AlterModelOptions(
            name='registrar',
            options={'verbose_name': 'Registrar', 'verbose_name_plural': 'Registrars'},
        ),
        migrations.AlterModelOptions(
            name='subdomain',
            options={'verbose_name': 'Subdomain', 'verbose_name_plural': 'Subdomains'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'verbose_name': 'Vendor', 'verbose_name_plural': 'Vendors'},
        ),
        migrations.AlterModelOptions(
            name='website',
            options={'verbose_name': 'Website', 'verbose_name_plural': 'Websites'},
        ),
        migrations.RemoveField(
            model_name='connectiontype',
            name='description',
        ),
        migrations.RemoveField(
            model_name='devicetype',
            name='description',
        ),
    ]
