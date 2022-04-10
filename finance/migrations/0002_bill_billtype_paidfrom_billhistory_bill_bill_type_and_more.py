# Generated by Django 4.0.3 on 2022-04-10 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('due_day', models.SmallIntegerField(default=1)),
                ('monthly_payments', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('current_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('apr', models.DecimalField(decimal_places=3, default=0.0, max_digits=5)),
                ('variable_payment', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='BillType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PaidFrom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BillHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.billtype'),
        ),
        migrations.AddField(
            model_name='bill',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='finance.organisation'),
        ),
        migrations.AddField(
            model_name='bill',
            name='paid_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='finance.paidfrom'),
        ),
    ]
