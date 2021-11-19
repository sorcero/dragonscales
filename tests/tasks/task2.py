from dragonscales import tasks


class Task(tasks.BaseTask):
    def run(self, a: int, b: str, c: dict):
        c[b] = a
        return c
