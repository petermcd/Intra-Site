# Generated by Django 4.0.3 on 2022-04-15 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_subdomain_hosted_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='alias',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
