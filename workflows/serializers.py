from typing import Iterable, Union

from rest_framework import serializers

from .models import Workflow


class WorkflowSerializer(serializers.Serializer[Union[Workflow, Iterable[Workflow]]]):
    name = serializers.CharField()
    author = serializers.CharField()
    cwl_version = serializers.CharField()
    created = serializers.DateTimeField()
