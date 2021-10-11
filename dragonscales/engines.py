import os

from rq import Queue
from redis import client

from . import schemas


class Engine(object):
    def __init__(self):
        self._tasks = {}
        self._queues = {}
        self._storages = {}
        self._callbacks = {}

        self._path = os.environ.get("DRAGONSCALES_PROJECT_PATH")
        self._url = os.environ.get("DRAGONSCALES_REDIS_URL", "redis://localhost:6379")

        self._redis = client.Redis.from_url(self._url)
        self._project = schemas.Project.parse_file(self._path)

        for queue in self._project.queues:
            self._queues[queue.name] = Queue(queue.name, connection=self._redis, **queue.args)

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
            callback.params,
        )

        return job

    def fetch(self, id):
        for queue in self._queues.values():
            if job := queue.fetch_job(id):
                return job

        return None
