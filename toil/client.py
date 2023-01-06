from io import BytesIO
from typing import Optional, Any, TypedDict
from enum import StrEnum

import requests

from .requests import RunWorkflow
from .responses import RunInfo, StartRun


class ToilClient:
    """Client to interact with Toil, documentation can be found
    [here](https://ga4gh.github.io/workflow-execution-service-schemas/docs/)
    """

    url: str
    engine_parameters: dict[str, Optional[str]]

    def __init__(
        self, host: str, port: int, settings: Optional[dict[str, Optional[str]]] = None
    ):
        self.url = f"{host}:{port}"
        if settings:
            self.engine_parameters = settings
        else:
            self.engine_parameters = {}

    def _build_url(self, suffix: str) -> str:
        return f"http://{self.url}/ga4gh/wes/v1/{suffix}"

    def run_workflow(  # type: ignore[misc]
        self,
        name: str,
        inputs: dict[str, Any],
        attachments: Optional[list[tuple[str, BytesIO]]],
    ) -> StartRun:
        # workflow_attachment needs to be handled separately from the other parameters
        # because of how requests deals with file uploads
        if attachments:
            files = map(lambda a: ("workflow_attachment", a), attachments)
        else:
            files = None
        payload = RunWorkflow(
            workflow_url=name,
            workflow_type="cwl",
            # TODO: give this a real value
            workflow_type_version="v1.2",
            workflow_params=inputs,
            workflow_engine_parameters=self.engine_parameters,
        )
        resp = requests.post(
            self._build_url("runs"),
            data=payload.toil_param_format(),
            files=files,
        )
        return StartRun.parse_raw(resp.text)

    def get_run_log(self, run_id: str) -> RunInfo:
        url = f"{self._build_url('runs')}/{run_id}"
        resp = requests.get(url)
        return RunInfo.parse_raw(resp.text)
