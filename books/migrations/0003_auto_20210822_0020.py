# Generated by Django 3.2.6 on 2021-08-21 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20210822_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='images',
        ),
        migrations.AddField(
            model_name='book',
            name='thumbnail',
            field=models.URLField(default=None, max_length=255),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
