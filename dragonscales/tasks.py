from pydantic import BaseModel


class BaseTask(BaseModel):

    queue: str

    def private_run(self, storage, callback, **params):
        result = self.run(**params)
        location = storage.store(result)

        callback.call(location)

        return location

    def run(self):
        raise NotImplementedError
