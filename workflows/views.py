from typing import TYPE_CHECKING, Sequence, Union, Optional

from django.http import FileResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from freva.requests import authed_user

from .forms import WorkflowUploadForm, WorkflowUpdateForm
from .models import Workflow
from .serializers import WorkflowSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import (
        _PermissionClass,  # type: ignore [reportPrivateUsage]
    )


class WorkflowList(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(
        self, _request: Request, username: str, _format: Optional[str] = None
    ) -> Response:
        user = User.objects.filter(username=username).first()
        if user is None:
            raise NotFound()
        workflows = Workflow.objects.filter(author=user)
        return Response(WorkflowSerializer(workflows, many=True).data)

    def post(
        self, request: Request, username: str, _format: Optional[str] = None
    ) -> Response:
        user = authed_user(request)
        if user.username != username:
            # TODO: not accurate, this is an authorization issue but maybe this should
            # be handled via permission_classes
            raise NotAuthenticated()
        form = WorkflowUploadForm(request.POST, request.FILES)
        # TODO: check that the workflow is valid
        # TODO: either get the cwl file version from the user or extract from the file
        if not form.is_valid():
            return Response(
                exception=True, status=status.HTTP_400_BAD_REQUEST, data=form.errors
            )
        already_exists = Workflow.objects.filter(name=form.cleaned_data["name"]).first()
        if not already_exists is None:
            # Don't allow duplicate workflows of the same name
            return Response(exception=True, status=status.HTTP_409_CONFLICT)
        workflow = Workflow(data=form.cleaned_data["file"])
        workflow.name = form.cleaned_data["name"]
        workflow.author = user
        workflow.save()
        return Response(status=status.HTTP_201_CREATED)


class WorkflowDetail(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(
        self,
        request: Request,
        username: str,
        workflow_id: str,
        _format: Optional[str] = None,
    ) -> Response:
        user = authed_user(request)
        if user.username != username:
            # TODO: not accurate, this is an authorization issue but maybe this should
            # be handled via permission_classes
            raise NotAuthenticated()
        workflow = Workflow.objects.filter(name=workflow_id, author=user).first()
        if workflow is None:
            raise NotFound()
        return Response(WorkflowSerializer(workflow).data)


class WorkflowFile(APIView):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def get(
        self,
        request: Request,
        username: str,
        workflow_id: str,
        format: Optional[str] = None,
    ) -> FileResponse:
        user = authed_user(request)
        if user.username != username:
            raise NotAuthenticated()
        workflow = Workflow.objects.filter(name=workflow_id, author=user).first()
        if workflow is None:
            raise NotFound()
        return FileResponse(workflow.data.file)

    def put(
        self,
        request: Request,
        username: str,
        workflow_id: str,
        _format: Optional[str] = None,
    ) -> Response:
        user = authed_user(request)
        if user.username != username:
            raise NotAuthenticated()
        workflow = Workflow.objects.filter(name=workflow_id, author=user).first()
        if workflow is None:
            raise NotFound()
        form = WorkflowUpdateForm(request.POST, request.FILES)
        # TODO: check that the workflow is valid
        # TODO: either get the cwl file version from the user or extract from the file
        if not form.is_valid():
            return Response(
                exception=True, status=status.HTTP_400_BAD_REQUEST, data=form.errors
            )
        workflow.data = form.cleaned_data["file"]
        workflow.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
