import json

from dragonscales import callbacks


class Callback(callbacks.BaseCallback):
    def call(self, location):
        callback_path = "/tmp/dragonscale.callback"
        with open(callback_path, "w") as callback_file:
            callback_file.write(json.dumps(location))
