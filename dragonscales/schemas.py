# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Sorcero, Inc.
#
# This file is part of Sorcero's Language Intelligence platform
# (see https://www.sorcero.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

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
