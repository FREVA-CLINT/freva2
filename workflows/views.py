from typing import Sequence, TYPE_CHECKING, Union

from django.http import FileResponse, HttpRequest
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ViewSet

from workflows.forms import WorkflowUploadForm
from workflows.models import Workflow
from .serializers import WorkflowSerializer

if TYPE_CHECKING:
    from rest_framework.permissions import _PermissionClass


class WorkflowViewSet(ViewSet):
    permission_classes: Sequence["_PermissionClass"] = [IsAuthenticated]

    def list(self, request: HttpRequest) -> Response:
        workflows = Workflow.objects.all()
        return Response(WorkflowSerializer(workflows, many=True).data)

    def retrieve(self, _request: HttpRequest, pk: str) -> Response:
        workflow = Workflow.objects.filter(name=pk).first()
        return Response(WorkflowSerializer(workflow).data)

    def create(self, request: HttpRequest) -> Response:
        form = WorkflowUploadForm(request.POST, request.FILES)
        # TODO: check that the workflow is valid
        # TODO: either get the cwl file version from the user or extract from the file
        if form.is_valid():
            file = request.FILES["file"]
            workflow = Workflow(data=file)
            workflow.name = form.cleaned_data["name"]
            # TODO: try to figure out the types here for mypy to accept this
            workflow.author = request.user  # type: ignore [assignment]
            workflow.save()
            # TODO: maybe make a better response
            return Response({"success": True})
        return Response({"success": False})

    @action(detail=True, methods=["get"])
    def workflow(self, _request: HttpRequest, pk: str) -> Union[Response, FileResponse]:
        workflow = Workflow.objects.filter(name=pk).first()
        if workflow is None:
            raise NotFound()
        return FileResponse(workflow.data.file)
