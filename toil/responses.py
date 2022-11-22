from pydantic import BaseModel


class StartRunResponse(BaseModel):
    run_id: str


class RunInfoResponse(BaseModel):
    # TODO: properly type this
    run_id: str
    request: dict
    state: str
    run_log: dict
    task_log: list
    outputs: dict
