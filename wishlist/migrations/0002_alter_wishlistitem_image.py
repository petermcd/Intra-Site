# Generated by Django 4.1.6 on 2023-04-23 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
