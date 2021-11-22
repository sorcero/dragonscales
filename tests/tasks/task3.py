from dragonscales import tasks


class Task(tasks.BaseTask):
    def run(self):
        raise Exception("task3 - Always fail")
