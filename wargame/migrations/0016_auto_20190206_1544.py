# Generated by Django 2.1.5 on 2019-02-06 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("wargame", "0015_auto_20190206_1538")]

    operations = [migrations.AlterUniqueTogether(name="submission", unique_together={("user_challenge", "value")})]
