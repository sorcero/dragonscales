from dragonscales import callbacks


class Callback(callbacks.BaseCallback):
    def call(self, storage_information):
        callback_path = "/tmp/dragonscale.callback"
        with open(callback_path, "w") as callback_file:
            callback_file.write(storage_information)
            
        return {"key": "value"}
