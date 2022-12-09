from typing import TYPE_CHECKING, Sequence, Union

from django.http import FileResponse
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.request import Request
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .forms import WorkflowUploadForm
from .models import Workflow
from .serializers import WorkflowSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import (
        _PermissionClass,  # type: ignore [reportPrivateUsage]
    )


class WorkflowViewSet(ViewSet):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def list(self, _request: Request) -> Response:
        workflows = Workflow.objects.all()
        return Response(WorkflowSerializer(workflows, many=True).data)

    def retrieve(self, _request: Request, pk: str) -> Response:
        workflow = Workflow.objects.filter(name=pk).first()
        return Response(WorkflowSerializer(workflow).data)

    def create(self, request: Request) -> Response:
        form = WorkflowUploadForm(request.POST, request.FILES)
        # TODO: check that the workflow is valid
        # TODO: either get the cwl file version from the user or extract from the file
        if not form.is_valid():
            return Response(
                exception=True, status=status.HTTP_400_BAD_REQUEST, data=form.errors
            )
        workflow = Workflow(data=form.cleaned_data["file"])
        workflow.name = form.cleaned_data["name"]
        match request.user:
            case User() as user:
                pass
            case _:
                raise NotAuthenticated()
        workflow.author = user
        workflow.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def workflow(self, _request: Request, pk: str) -> Union[Response, FileResponse]:
        workflow = Workflow.objects.filter(name=pk).first()
        if workflow is None:
            raise NotFound()
        return FileResponse(workflow.data.file)
