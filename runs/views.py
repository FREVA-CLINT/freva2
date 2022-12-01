import io
from typing import TYPE_CHECKING, Sequence

from django.http import HttpRequest
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from freva import settings
from toil.client import RunWorkflow, ToilClient
from workflows.models import Workflow

from .models import Run
from .serializers import CreateRunSerializer, RunSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass  # type: ignore [reportPrivateUsage]


class RunViewSet(ViewSet):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def list(self, request: HttpRequest) -> Response:
        runs = Run.objects.all()
        return Response(RunSerializer(runs, many=True).data)

    def create(self, request: HttpRequest) -> Response:
        toil = ToilClient(settings.TOIL["host"], settings.TOIL["port"])
        stream = io.BytesIO(request.body)
        data = JSONParser().parse(stream)

        serializer = CreateRunSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        opts = serializer.data
        workflow = Workflow.objects.filter(name=opts["workflow_name"]).first()
        if workflow is None:
            raise NotFound("referenced workflow does not exist")

        # this isn't ideal but currently toil doesn't support authenticated
        # workflow_urls meaning that our only option is to either have them all
        # public or upload all workflow files for each run
        contents = workflow.data.read()
        workflow_files = [(workflow.data.name, contents)]
        run_response = toil.run_workflow(
            RunWorkflow(
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

    def retrieve(self, request: HttpRequest, pk: str) -> Response:
        run = Run.objects.filter(id=pk).first()
        if run is None:
            raise NotFound
        return Response(RunSerializer(run).data)

    @action(detail=True, methods=["get"])
    def status(self, _request: HttpRequest, pk: str) -> Response:
        toil = ToilClient(settings.TOIL["host"], settings.TOIL["port"])
        run = Run.objects.filter(id=pk).first()
        if run is None:
            raise NotFound
        toil_info = toil.get_run_log(run.id)
        return Response(toil_info.dict())
