from django.contrib.auth.models import User
from django.db.models import (
    DO_NOTHING,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
)
from django.utils.timezone import datetime


def user_workflow_path(instance: "Workflow", filename: str) -> str:
    user_id = instance.author.get_username()
    return f"workflows/{user_id}/{filename}"


class Workflow(Model):
    name = CharField(max_length=64)
    cwl_version = CharField(max_length=5)
    created = DateTimeField(default=datetime.now)
    data: FileField = FileField(upload_to=user_workflow_path)
    author = ForeignKey(User, on_delete=DO_NOTHING)
