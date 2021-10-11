from pydantic import BaseModel


class BaseAuthorizer(BaseModel):
    class Config:
        extra = "allow"

    def authorize(self, request):
        raise NotImplementedError
