from django.forms import CharField, FileField, Form


class WorkflowUploadForm(Form):
    name: CharField = CharField(max_length=64, required=True)
    file: FileField = FileField(required=True)
