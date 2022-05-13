# Generated by Django 4.0.3 on 2022-04-17 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_application_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='operatingsystem',
            name='alias',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.CreateModel(
            name='AdditionalAnsibleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('alias', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network.additionalansiblegroup')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='additional_ansible_groups',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='network.additionalansiblegroup'),
        ),
    ]