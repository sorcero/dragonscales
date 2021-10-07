from typing import List, Union
from pydantic import BaseModel


class TaskDef(BaseModel):

    name: str
    queue: str
    module: str
    args: dict


class Project(BaseModel):

    tasks: List[TaskDef]


class TaskReq(BaseModel):

    name: str
    params: dict


class JobRequest(BaseModel):

    task: TaskReq


class JobStatus(BaseModel):

    id: str
    status: str
    result: Union[dict, None]
