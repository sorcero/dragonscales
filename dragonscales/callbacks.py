from pydantic import BaseModel


class BaseCallback(BaseModel):
    class Config:
        extra = "allow"

    def call(self):
        raise NotImplementedError
