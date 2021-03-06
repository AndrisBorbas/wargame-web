import json
import os
from fractions import Fraction

from chunked_upload.models import ChunkedUpload
from django.db import models
from django.db.models import Model, CharField, Manager, TextField, signals
# noinspection PyMethodMayBeStatic
from django.dispatch import receiver


class ConfigManager(Manager):
    def is_qpa(self):
        return Config.objects.get(key="qpa_hack").value == "qpa"

    def config_name(self):
        return Config.objects.get(key="qpa_hack")

    def stage_tasks(self):
        return Config.objects.get(key="stage_tasks").get_int()

    def registration_disabled(self):
        return Config.objects.get(key="disable_registration").get_bool()

    def wargame_active(self):
        return Config.objects.get(key="wargame_active").get_bool()

    def show_qpa_points(self):
        return Config.objects.get(key="show_qpa_points").get_bool()

    def qpa_points_multiplier(self):
        return Config.objects.get(key="qpa_points_multiplier").get_float()

    def email_required(self):
        return Config.objects.get(key="email_required").get_bool()

    def private_scoreboard(self):
        return Config.objects.get(key="private_scoreboard").get_bool()


class Config(Model):
    key = CharField(max_length=255, primary_key=True)
    value = CharField(max_length=255)
    display_name = CharField(max_length=255)
    description = CharField(max_length=255, blank=True, default="")
    possible_values = CharField(max_length=500, blank=True, default="")
    objects = ConfigManager()

    def get_int(self):
        return int(self.value)

    def get_bool(self):
        return self.value == "True"

    def get_float(self):
        try:
            return float(self.value)
        except ValueError:
            return float(Fraction(self.value))

    def get_possible_values(self):
        if self.possible_values is "":
            return None
        return json.loads(self.possible_values)

    def set_possible_values(self, values):
        self.possible_values = json.dumps(values)


class ChallengeFileChunkedUpload(ChunkedUpload):
    pass


class StaticContent(Model):
    key = CharField(max_length=255, primary_key=True)
    display_name = CharField(max_length=255)
    note = CharField(max_length=255, default="")
    html = TextField()


class Export(Model):
    EXPORT_STATUS = (("IN_PROGRESS", "In progress"), ("DONE", "Done"), ("FAILED", "Failed"))
    started_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="exports/", null=True)
    status = models.CharField(max_length=20, choices=EXPORT_STATUS, default="IN_PROGRESS")


# Deletes file from filesystem when File object is deleted.
@receiver(signals.post_delete, sender=Export)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
