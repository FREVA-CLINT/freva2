from django.forms import Form, CharField, FileField


class WorkflowUploadForm(Form):
    name: CharField = CharField(max_length=64, required=True)
    file: FileField = FileField(required=True)
