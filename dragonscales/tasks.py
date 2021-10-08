from pydantic import BaseModel

class BaseTask(BaseModel):

    queue: str

    def run(self):
        raise NotImplementedError
