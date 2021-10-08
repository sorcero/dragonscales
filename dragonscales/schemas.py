from typing import List, Union
from pydantic import BaseModel


class TaskDef(BaseModel):

    name: str
    queue: str
    module: str
    args: dict


class Project(BaseModel):

    tasks: List[TaskDef]


class TaskRef(BaseModel):

    name: str
    params: dict


class JobRequest(BaseModel):

    task: TaskRef


class JobStatus(BaseModel):

    id: str
    status: str
    result: Union[dict, None]


class StorageDef(BaseModel):

    name: str
    module: str
    args: dict


class StorageRef(BaseModel):

    name: str
    params: dict


class CallbackDef(BaseModel):

    name: str
    module: str
    args: dict


class CallbackRef(BaseModel):

    name: str
    params: dict
