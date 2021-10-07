import os

from rq import Queue
from redis import client

from . import schemas


class Engine(object):
    def __init__(self):
        self._tasks = {}
        self._queues = {}

        self._path = os.environ.get("DRAGONSCALES_PROJECT_PATH")
        self._url = os.environ.get("DRAGONSCALES_REDIS_URL", "redis://localhost:6379")

        self._redis = client.Redis.from_url(self._url)
        self._project = schemas.Project.parse_file(self._path)

        for task in self._project.tasks:
            module = __import__(task.module, fromlist=[None])
            instance = module.Task(**task.args)

            self._tasks[task.name] = instance

            # XXX keep track of which queue is used by this task
            setattr(instance, "queue", task.queue)

            if self._queues.get(task.queue) is not None:
                continue

            self._queues[task.queue] = Queue(task.queue, connection=self._redis)

    def enqueue(self, task):
        instance = self._tasks.get(task.name)
        queue = self._queues.get(instance.queue)

        job = queue.enqueue(instance.run, **task.params)

        return job

    def fetch(self, id):
        for queue in self._queues.values():
            if job := queue.fetch_job(id):
                return job

        return None
