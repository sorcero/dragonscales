from pydantic import BaseModel


class BaseStorage(BaseModel):
    class Config:
        extra = "allow"

    def store(self):
        raise NotImplementedError
