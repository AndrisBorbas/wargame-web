# Generated by Django 2.0.3 on 2018-08-09 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wargame', '0007_file_display_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
