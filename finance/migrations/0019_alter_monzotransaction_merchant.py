# Generated by Django 4.1.6 on 2023-02-16 23:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0018_alter_investments_date_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monzotransaction',
            name='merchant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.monzomerchant'),
        ),
    ]
