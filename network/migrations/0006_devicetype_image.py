# Generated by Django 4.0.3 on 2022-04-11 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_device_applications'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='image',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]