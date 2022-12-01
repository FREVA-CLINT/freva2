from django.db.models import DO_NOTHING, CharField, ForeignKey, Model

from workflows.models import Workflow


class Run(Model):
    id: CharField[str] = CharField(max_length=36, primary_key=True)
    workflow: ForeignKey[Workflow] = ForeignKey(Workflow, on_delete=DO_NOTHING)
