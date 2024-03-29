# Generated by Django 4.1.6 on 2023-02-23 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_remove_accommodation_check_in_before_checkout_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='event',
            name='event_ends_after_start',
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('ends__gte', models.F('start')))), name='event_ends_after_start'),
        ),
    ]
