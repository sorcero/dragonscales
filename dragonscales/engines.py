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

import os

from rq import Queue
from rq.command import send_stop_job_command
from redis import client
from fastapi import Request, status, HTTPException

from . import schemas
from .logger import logger


class Engine(object):
    def __init__(self):
        self._tasks = {}
        self._queues = {}
        self._storages = {}
        self._callbacks = {}
        self._authorizer = None

        self._path = os.environ.get("DRAGONSCALES_PROJECT_PATH")
        self._url = os.environ.get("DRAGONSCALES_REDIS_URL", "redis://localhost:6379")

        logger.debug(
            "initializing",
            extra={"props": {"project": self._path, "service": self._url}},
        )

        self._redis = client.Redis.from_url(self._url)
        self._project = schemas.Project.parse_file(self._path)

        for queue in self._project.queues:
            self._queues[queue.name] = Queue(
                queue.name, connection=self._redis, **queue.args
            )

        for task in self._project.tasks:
            module = __import__(task.module, fromlist=[None])
            instance = module.Task(queue=task.queue, **task.args)
            self._tasks[task.name] = instance

        for storage in self._project.storages:
            module = __import__(storage.module, fromlist=[None])
            instance = module.Storage(**storage.args)
            self._storages[storage.name] = instance

        for callback in self._project.callbacks:
            module = __import__(callback.module, fromlist=[None])
            instance = module.Callback(**callback.args)
            self._callbacks[callback.name] = instance

        authorizer = self._project.authorizer
        module = __import__(authorizer.module, fromlist=[None])
        self._authorizer = module.Authorizer(**authorizer.args)

    def enqueue(self, task, storage, callback):
        task_instance = self._tasks.get(task.name)
        storage_instance = self._storages.get(storage.name)
        callback_instance = self._callbacks.get(callback.name)
        queue = self._queues.get(task_instance.queue)

        job = queue.enqueue(
            task_instance.private_run,
            storage_instance,
            callback_instance,
            task.params,
            storage.params,
            callback.params,
        )

        return job

    def fetch(self, id):
        job = None

        for queue in self._queues.values():
            if job := queue.fetch_job(id):
                break

        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )

        return job

    def get_jobs(self):
        jobs = set()

        for queue in self._queues.values():
            for registry in [
                "started_job_registry",
                "deferred_job_registry",
                "finished_job_registry",
                "failed_job_registry",
                "scheduled_job_registry",
            ]:
                jobs.update(getattr(queue, registry).get_job_ids())

        return jobs

    def cancel(self, id):
        job = self.fetch(id)

        if job is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found",
            )

        # stop if it's currently running
        try:
            send_stop_job_command(self._redis, job.id)
        except Exception:
            job.cancel()
        job.delete()

    async def authorize(self, request: Request):
        return self._authorizer.authorize(request)
