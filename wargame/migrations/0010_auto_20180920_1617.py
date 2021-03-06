# Generated by Django 2.1.1 on 2018-09-20 14:17

from django.db import migrations, models
import wargame.models


class Migration(migrations.Migration):

    dependencies = [("wargame", "0009_auto_20180919_1923")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[wargame.models.custom_username_validator],
                verbose_name="username",
            ),
        )
    ]
