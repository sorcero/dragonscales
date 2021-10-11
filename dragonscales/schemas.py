from typing import List, Union
from pydantic import BaseModel


class TaskDef(BaseModel):

    name: str
    queue: str
    module: str
    args: dict


class StorageDef(BaseModel):

    name: str
    module: str
    args: dict


class CallbackDef(BaseModel):

    name: str
    module: str
    args: dict


class AuthorizerDef(BaseModel):

    name: str
    module: str
    args: dict


class QueueDef(BaseModel):

    name: str
    args: dict


class Project(BaseModel):

    queues: List[QueueDef]
    tasks: List[TaskDef]
    storages: List[StorageDef]
    callbacks: List[CallbackDef]
    authorizer: AuthorizerDef


class TaskRef(BaseModel):

    name: str
    params: dict


class StorageRef(BaseModel):

    name: str
    params: dict


class CallbackRef(BaseModel):

    name: str
    params: dict


class JobRequest(BaseModel):

    task: TaskRef
    storage: StorageRef
    callback: CallbackRef


class JobStatus(BaseModel):

    id: str
    status: str
    result: Union[dict, None]
