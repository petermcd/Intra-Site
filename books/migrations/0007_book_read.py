# Generated by Django 3.2.6 on 2021-08-22 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_alter_book_isbn13'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]