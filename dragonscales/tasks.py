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

from pydantic import BaseModel
from rq import get_current_job

from .logger import logger


class BaseTask(BaseModel):
    class Config:
        extra = "allow"

    queue: str

    def private_run(self, storage, task_params, storage_params):
        try:
            result = self.run(**task_params)
            location = storage.store(result, **storage_params)
        except Exception as e:
            job = get_current_job()
            logger.error(
                "error",
                extra={
                    "props": {
                        "job_id": job.id,
                        "error": str(e),
                    }
                },
            )
            raise e

        return location

    def run(self):
        raise NotImplementedError
