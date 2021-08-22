# Generated by Django 3.2.6 on 2021-08-21 23:03

from django.db import migrations, models
import django.db.models.deletion


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
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(max_length=500)),
                ('publisher', models.CharField(max_length=200)),
                ('published', models.DateField()),
                ('isbn10', models.IntegerField(max_length=10)),
                ('isbn13', models.IntegerField(max_length=13)),
                ('description', models.CharField(max_length=2000)),
                ('pages', models.IntegerField(max_length=5)),
                ('authors', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.image')),
            ],
        ),
    ]
