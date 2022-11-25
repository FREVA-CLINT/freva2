from rest_framework import serializers


class WorkflowSerializer(serializers.Serializer):
    name = serializers.CharField()
    author = serializers.CharField()
    cwl_version = serializers.CharField()
    created = serializers.DateTimeField()
