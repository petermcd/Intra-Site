# Generated by Django 4.0.3 on 2022-04-14 22:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0006_alter_investments_investment_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'verbose_name': 'Bill', 'verbose_name_plural': 'Bills'},
        ),
        migrations.AlterModelOptions(
            name='billtype',
            options={'verbose_name': 'Bill type', 'verbose_name_plural': 'Bill types'},
        ),
        migrations.AlterModelOptions(
            name='investments',
            options={'verbose_name': 'Investment', 'verbose_name_plural': 'Investments'},
        ),
        migrations.AlterModelOptions(
            name='organisation',
            options={'verbose_name': 'Organisation', 'verbose_name_plural': 'Organisations'},
        ),
        migrations.AlterModelOptions(
            name='paidfrom',
            options={'verbose_name': 'Paid from', 'verbose_name_plural': 'Paid from'},
        ),
        migrations.RemoveField(
            model_name='bill',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='description',
        ),
    ]
