# Generated by Django 4.1.6 on 2023-04-23 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0002_alter_wishlistitem_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistitem',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
