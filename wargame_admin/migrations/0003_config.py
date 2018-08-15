# Generated by Django 2.0.3 on 2018-08-15 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wargame_admin', '0002_delete_config'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('key', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=255)),
                ('display_name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('possible_values', models.CharField(blank=True, default='', max_length=500)),
            ],
        ),
    ]
