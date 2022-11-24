import json
from dataclasses import dataclass
from io import BytesIO
from typing import Any, Optional

import requests

from .responses import StartRun, RunInfo
from .requests import RunWorkflow


class ToilClient:
    """Client to interact with Toil, documentation can be found
    [here](https://ga4gh.github.io/workflow-execution-service-schemas/docs/)
    """

    url: str

    def __init__(self, host: str, port: int):
        self.url = f"{host}:{port}"

    def _build_url(self, suffix: str) -> str:
        return f"http://{self.url}/ga4gh/wes/v1/{suffix}"

    def run_workflow(
        self,
        payload: RunWorkflow,
        attachments: Optional[list[tuple[str, BytesIO]]],
    ) -> StartRun:
        # workflow_attachment needs to be handled separately from the other parameters
        # because of how requests deals with file uploads
        if attachments:
            files = map(lambda a: ("workflow_attachment", a), attachments)
        else:
            files = None
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
