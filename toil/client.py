from io import BytesIO
from typing import Any, Optional

import requests

from .requests import RunWorkflow
from .responses import RunInfo, StartRun


class ToilClient:
    """Client to interact with Toil, documentation can be found
    [here](https://ga4gh.github.io/workflow-execution-service-schemas/docs/)
    """

    url: str
    engine_parameters: dict[str, Optional[str]]

    def __init__(self, host: str, port: int, settings: dict[str, Optional[str]]):
        self.url = f"{host}:{port}"
        self.engine_parameters = settings

    def _build_wes_url(self, suffix: str) -> str:
        return f"http://{self.url}/ga4gh/wes/v1/{suffix}"

    def _build_toil_url(self, suffix: str) -> str:
        """Build url for endpoints that are specific to toil and not part of the GA4GH
        WES spec
        """
        return f"http://{self.url}/toil/wes/v1/{suffix}"

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
            self._build_wes_url("runs"),
            data=payload.toil_param_format(),
            files=files,
        )
        return StartRun.parse_raw(resp.text)

    def get_run_log(self, run_id: str) -> RunInfo:
        url = f"{self._build_wes_url('runs')}/{run_id}"
        resp = requests.get(url)
        return RunInfo.parse_raw(resp.text)

    def get_stdout(self, run_id: str) -> str:
        url = f"{self._build_toil_url('logs')}/{run_id}/stdout"
        resp = requests.get(url)
        return resp.text

    def get_stderr(self, run_id: str) -> str:
        url = f"{self._build_toil_url('logs')}/{run_id}/stderr"
        resp = requests.get(url)
        return resp.text
