# Generated by Django 3.2.6 on 2021-09-03 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('at', models.DateField(auto_now_add=True)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.company')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.IntegerField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.company')),
            ],
        ),
    ]