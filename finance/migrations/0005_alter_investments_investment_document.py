# Generated by Django 4.0.3 on 2022-04-13 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_rename_transaction_value_billhistory_current_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investments',
            name='investment_document',
            field=models.FileField(blank=True, null=True, upload_to='documents/investments/'),
        ),
    ]
