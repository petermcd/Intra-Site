# Generated by Django 4.0.3 on 2022-04-11 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_application_name_alter_connectiontype_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='vendor',
            new_name='hardware_vendor',
        ),
    ]
