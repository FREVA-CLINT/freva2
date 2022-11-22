import io
from typing import TYPE_CHECKING, Sequence

from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    DictField,
    Serializer,
    SlugRelatedField,
)
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import NotFound
from rest_framework.reverse import reverse

from workflows.models import Workflow
from toil.client import RequestPayload, ToilClient
from runs.models import Run

if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass


class RunViewSet(ViewSet):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def list(self, request: HttpRequest) -> Response:
        runs = Run.objects.all()
        return Response(RunSerializer(runs, many=True).data)

    def create(self, request: HttpRequest) -> Response:
        toil = ToilClient("wes-server", 8001)
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        serializer = CreateRunSerializer(data=data)
        if serializer.is_valid():
            opts = serializer.data
            workflow = Workflow.objects.filter(name=opts["workflow_name"]).first()
            if workflow is None:
                raise NotFound("referenced workflow does not exist")

            # this isn't ideal but currently toil doesn't support authenticated
            # workflow_urls meaning that our only option is to either have them all
            # public or upload all workflow files for each run
            contents = workflow.data.read()
            workflow_files = [(workflow.data.name, contents)]
            run_response = toil.start_run(
                RequestPayload(
                    workflow_url=workflow.data.name,
                    workflow_type="cwl",
                    workflow_type_version="v1.2",
                    workflow_params=opts["inputs"],
                ),
                workflow_files,
            )
            run = Run(id=run_response.run_id, workflow=workflow)
            run.save()
            return Response(RunSerializer(run).data)
        else:
            return Response(serializer.errors)

    def retrieve(self, request: HttpRequest, pk: str) -> Response:
        run = Run.objects.filter(id=pk).first()
        if run is None:
            raise NotFound
        return Response(RunSerializer(run).data)


class CreateRunSerializer(Serializer):
    workflow_name: CharField = CharField()
    # TODO: it might be useful to check this against the expected inputs to the workflow
    inputs: DictField = DictField()


class RunSerializer(Serializer):
    id: CharField = CharField()
    workflow: SlugRelatedField = SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
