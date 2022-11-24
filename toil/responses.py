from typing import Any, Optional

from pydantic import BaseModel

from .requests import RunWorkflow


class StartRun(BaseModel):
    run_id: str


class RunInfo(BaseModel):
    # TODO: properly type this
    run_id: str
    request: RunWorkflow
    state: str
    run_log: "RunLog"
    task_logs: list["TaskLog"]
    # this is a structure object but the documentation doesn't say how, need to figure
    # that out
    outputs: dict[str, Any]


class RunLog(BaseModel):
    name: Optional[str]
    cmd: list[str]
    start_time: str
    end_time: str
    stdout: str
    stderr: str
    exit_code: int


class TaskLog(BaseModel):
    name: str
    cmd: list[str]
    start_time: str
    end_time: str
    stdout: str
    stderr: str
    exit_code: int


RunInfo.update_forward_refs()
