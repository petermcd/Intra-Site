# Generated by Django 4.0.3 on 2022-08-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0011_monzo_last_fetched_datetime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monzo",
            name="last_fetched_datetime",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
