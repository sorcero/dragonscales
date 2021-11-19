import json

from dragonscales import callbacks


class Callback(callbacks.BaseCallback):
    def call(self, location, y: str):
        callback_path = "/tmp/dragonscale.callback"
        y += " - test"
        with open(callback_path, "w") as callback_file:
            callback_file.write(json.dumps(location))
