from pydantic import BaseModel

class BaseCallback(BaseModel):
    def call(self):
        raise NotImplementedError
