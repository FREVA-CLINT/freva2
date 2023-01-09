from typing import TYPE_CHECKING, Sequence

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from freva import settings
from toil.client import ToilClient
from workflows.models import Workflow

from .models import Run
from .serializers import CreateRunSerializer, RunSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import (
        _PermissionClass,  # type: ignore [reportPrivateUsage]
    )


class RunList(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(self, _request: Request) -> Response:
        runs = Run.objects.all()
        return Response(RunSerializer(runs, many=True).data)

    def post(self, request: Request) -> Response:
        toil = ToilClient(
            settings.TOIL["host"],
            settings.TOIL["port"],
            settings.TOIL["workflow_engine_settings"],
        )

        data = JSONParser().parse(request)
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

        # TODO: this also doesn't handle workflows consisting of multiple files
        contents = workflow.data.read()
        workflow_files = [(workflow.data.name, contents)]
        run_response = toil.run_workflow(
            workflow.data.name,
            opts["inputs"],
            workflow_files,
        )
        run = Run(id=run_response.run_id, workflow=workflow)
        run.save()
        return Response(RunSerializer(run).data)


class RunDetail(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(self, _request: Request, run_id: str) -> Response:
        run = Run.objects.filter(id=run_id).first()
        if run is None:
            raise NotFound
        return Response(RunSerializer(run).data)


class RunStatus(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(self, _request: Request, run_id: str) -> Response:
        toil = ToilClient(
            settings.TOIL["host"],
            settings.TOIL["port"],
            settings.TOIL["workflow_engine_settings"],
        )
        run = Run.objects.filter(id=run_id).first()
        if run is None:
            raise NotFound
        toil_info = toil.get_run_log(run.id)
        return Response(toil_info.dict())


class RunStdout(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(self, _request: Request, run_id: str) -> Response:
        toil = ToilClient(
            settings.TOIL["host"],
            settings.TOIL["port"],
            settings.TOIL["workflow_engine_settings"],
        )
        run = Run.objects.filter(id=run_id).first()
        if run is None:
            raise NotFound
        stdout = toil.get_stdout(run_id)
        return Response(stdout)


class RunStderr(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(self, _request: Request, run_id: str) -> Response:
        toil = ToilClient(
            settings.TOIL["host"],
            settings.TOIL["port"],
            settings.TOIL["workflow_engine_settings"],
        )
        run = Run.objects.filter(id=run_id).first()
        if run is None:
            raise NotFound
        stderr = toil.get_stderr(run_id)
        return Response(stderr)
