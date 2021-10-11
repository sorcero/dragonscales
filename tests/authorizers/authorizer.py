from dragonscales import authorizers


class Authorizer(authorizers.BaseAuthorizer):
    def authorize(self, request):
        return {"user": "user"}
