# Generated by Django 3.2.6 on 2021-08-21 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn10',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn13',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages',
            field=models.IntegerField(),
        ),
    ]
