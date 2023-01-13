from django.db.models import DO_NOTHING, CharField, ForeignKey, Model

from workflows.models import Workflow


class Run(Model):
    # These will be identical to the run id created by Toil
    id: "CharField[str, str]" = CharField(max_length=36, primary_key=True)
    workflow: ForeignKey[Workflow, Workflow] = ForeignKey(
        Workflow, on_delete=DO_NOTHING
    )
