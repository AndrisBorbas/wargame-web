from django.forms import ModelForm, Form, CharField, TextInput, FileField, FileInput, Textarea, BooleanField
from djangocodemirror.fields import CodeMirrorField

from wargame.models import File, Challenge, User
from wargame_admin.models import StaticContent


class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ["display_name", "private", "config_name"]

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        # Remove the blank choice
        field = self.fields["config_name"]
        field.choices = field.choices[1:]


class FileUploadForm(ModelForm):
    class Meta:
        model = File
        fields = ["file", "display_name", "private", "config_name"]

    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        # Remove the blank choice
        field = self.fields["config_name"]
        field.choices = field.choices[1:]

        self.fields["file"].widget.attrs.update({"class": "hidden"})
        self.fields["file"].label = ""


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = [
            "title",
            "import_name",
            "hidden",
            "description",
            "short_description",
            "level",
            "flag_qpa",
            "flag_hacktivity",
            "points",
            "hint",
            "setup",
            "solution",
            "tags",
        ]
        help_texts = {
            "import_name": "A unique identifier that is a valid directory name",
            "hidden": "Hidden challenges do not contribute to users's score and cannot be accessed",
        }


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ["is_superuser", "hidden", "is_active"]
        labels = {"is_superuser": "Admin"}
        help_texts = {
            "is_superuser": "Allows the user to access the admin site and edit all objects in the django admin interface",
            "hidden": "Hides the user from the scoreboard",
        }


class ChallengeImportForm(Form):
    file = FileField(widget=FileInput(attrs={"accept": "application/zip"}), label="")
    dry_run = BooleanField(required=False)


class UserImportForm(Form):
    file = FileField(widget=FileInput(attrs={"accept": ".csv"}), label="")
    dry_run = BooleanField(required=False)


class StaticContentForm(ModelForm):
    html = CodeMirrorField(label="Text", config_name="html")

    class Meta:
        model = StaticContent
        fields = ["html"]


class RebalanceChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["level", "points"]
