from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from .requests import RunWorkflow


class StartRun(BaseModel):
    run_id: str


class RunInfo(BaseModel):
    run_id: str
    request: RunWorkflow
    state: "RunState"
    run_log: "RunLog"
    task_logs: list["TaskLog"]
    # the type here would depend on the workflow engine
    # for our cases this always be CWL so we may be able to give this a proper type in
    # the future
    outputs: dict[str, Any]  # type: ignore [misc]


class RunLog(BaseModel):
    name: Optional[str]
    cmd: list[str]
    start_time: str
    end_time: Optional[str]
    stdout: str
    stderr: str
    exit_code: Optional[int]


class TaskLog(BaseModel):
    name: str
    cmd: list[str]
    start_time: str
    end_time: str
    stdout: str
    stderr: str
    exit_code: int


class RunState(StrEnum):
    UNKNOWN = "UNKNOWN"
    QUEUED = "QUEUED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    EXECUTOR_ERROR = "EXECUTOR_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CANCELED = "CANCELED"
    CANCELING = "CANCELING"


RunInfo.update_forward_refs()
