from typing import Any, Mapping
from django.forms import Form, CharField, FileField


class WorkflowUploadForm(Form):
    name: CharField = CharField(max_length=64)
    file: FileField = FileField()
