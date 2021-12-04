# Generated by Django 3.2.7 on 2021-11-30 14:07

from django.db import migrations, models

import books.models
import Intranet.misc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, default=None, max_length=500)),
                ('publisher', models.CharField(max_length=200)),
                ('published', models.DateField()),
                ('isbn10', models.CharField(max_length=10, unique=True)),
                ('isbn13', models.CharField(max_length=13, unique=True)),
                ('description', models.CharField(max_length=5000)),
                ('pages', models.IntegerField()),
                ('thumbnail', models.URLField(blank=True, default=None, max_length=255)),
                ('ebook', models.FileField(blank=True, null=True, storage=Intranet.misc.OverwriteStorage, upload_to=books.models.content_file_name)),
                ('read', models.BooleanField(default=False)),
                ('authors', models.ManyToManyField(to='books.Author')),
            ],
        ),
    ]
