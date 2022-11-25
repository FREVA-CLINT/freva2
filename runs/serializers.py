from rest_framework.serializers import (
    CharField,
    DictField,
    Serializer,
    SlugRelatedField,
)


class CreateRunSerializer(Serializer):
    workflow_name: CharField = CharField()
    # TODO: it might be useful to check this against the expected inputs to the workflow
    inputs: DictField = DictField()


class RunSerializer(Serializer):
    id: CharField = CharField()
    workflow: SlugRelatedField = SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
