from pydantic import BaseModel


class BaseTask(BaseModel):

    class Config:
        extra = "allow"

    queue: str

    def private_run(self, storage, callback, task_params, callback_params):
        result = self.run(**task_params)
        location = storage.store(result)

        callback.call(location, **callback_params)

        return location

    def run(self):
        raise NotImplementedError
