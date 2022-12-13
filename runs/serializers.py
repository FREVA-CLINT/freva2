from typing import Any, Union, Iterable
from rest_framework.serializers import (
    CharField,
    DictField,
    Serializer,
    SlugRelatedField,
)

from workflows.models import Workflow
from .models import Run


# type ignore here is necessary because `Serializer` takes the type it's given to
# validate. In the case of json data, JsonParser.parse returns `dict[str, Any]` so
# I don't think there's any way to avoid this
class CreateRunSerializer(Serializer[dict[str, Any]]):  # type: ignore [misc]
    workflow_name: CharField = CharField()
    # TODO: it might be useful to check this against the expected inputs to the workflow
    inputs: DictField = DictField()


class RunSerializer(Serializer[Union[Run, Iterable[Run]]]):
    id: CharField = CharField()
    workflow: "SlugRelatedField[Workflow]" = SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
