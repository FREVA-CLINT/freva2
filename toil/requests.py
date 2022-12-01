import json
from typing import Any, Optional

from pydantic import BaseModel


class RunWorkflow(BaseModel):
    workflow_url: str
    workflow_type: str  # or enum that's serialized to a str?
    workflow_type_version: str
    workflow_params: dict[str, Any]
    workflow_engine_parameters: Optional[dict[str, Optional[str]]] = None
    tags: Optional[dict[str, str]] = None

    def toil_param_format(self) -> dict[str, str]:
        out: dict[str, str] = {
            "workflow_url": self.workflow_url,
            "workflow_type": self.workflow_type,
            "workflow_type_version": self.workflow_type_version,
            "workflow_params": json.dumps(self.workflow_params),
        }
        if self.workflow_engine_parameters:
            out["workflow_engine_parameters"] = json.dumps(
                self.workflow_engine_parameters
            )
        if self.tags:
            out["tags"] = json.dumps(self.tags)
        return out
