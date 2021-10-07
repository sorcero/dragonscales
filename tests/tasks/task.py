from dragonscales import tasks


class Task(tasks.BaseTask):
    def run(self):
        return {"key": "value"}
