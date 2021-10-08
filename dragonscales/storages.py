from pydantic import BaseModel

class BaseStorage(BaseModel):
    def store(self):
        raise NotImplementedError
