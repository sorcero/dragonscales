import json

from dragonscales import storages


class Storage(storages.BaseStorage):
    def store(self, result):
        storage_path = "/tmp/dragonscale.storage"
        with open(storage_path, "w") as storage_file:
            storage_file.write(json.dumps(result))
        return {"path": storage_path}
