import json
from io import BytesIO
from typing import Any, Optional
from dataclasses import dataclass

import requests
from pydantic import BaseModel, Field

from .responses import StartRunResponse


@dataclass
class RequestPayload:
    workflow_url: str
    workflow_type: str  # or enum that's serialized to a str
    workflow_type_version: str
    workflow_params: dict[str, Any]
    workflow_engine_parameters: Optional[dict[str, Optional[str]]] = None
    tags: Optional[dict[str, str]] = None

    def toil_param_format(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "workflow_url": self.workflow_url,
            "workflow_type": self.workflow_type,
            "workflow_type_version": self.workflow_type_version,
            "workflow_params": json.dumps(self.workflow_params),
        }
        if self.workflow_engine_parameters:
            out["workflow_engine_parameters"] = self.workflow_engine_parameters
        if self.tags:
            out["tags"] = self.tags
        return out


class ToilClient:
    url: str

    def __init__(self, host: str, port: int):
        self.url = f"{host}:{port}"

    def build_url(self, suffix: str) -> str:
        return f"http://{self.url}/ga4gh/wes/v1/{suffix}"

    def start_run(
        self,
        payload: RequestPayload,
        workflow_attachments: list[tuple[str, tuple[str, BytesIO, str]]],
    ) -> StartRunResponse:
        print(payload.toil_param_format())
        resp = requests.post(
            self.build_url("runs"),
            data=payload.toil_param_format(),
            files=workflow_attachments,
        )
        print(resp.text)
        return StartRunResponse.parse_raw(resp.text)
