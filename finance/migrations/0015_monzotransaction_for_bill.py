# Generated by Django 4.1 on 2022-08-18 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_alter_monzotransaction_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='monzotransaction',
            name='for_bill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='finance.bill'),
        ),
    ]
