from dragonscales import storages


class Storage(storages.BaseStorage):
    def store(self, result):
        raise Exception("storage3 - Always fail")
