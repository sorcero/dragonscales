# dragonscales :dragon:

`dragonscales` is a highly customizable asynchronous job-scheduler framework. This library is used to scale the execution of multiple tasks by multiple users. A developer can expose several predefined tasks that are available to the users through a jobs service, without the need to build the job system itself.

## Usage

### Service developer

As the developer, you need to populate the service with the tasks that will later be availble for the clients to run.

For each task you want to implement, a [BaseTask](dragonscales/tasks.py) subclass needs to be created along with its functionality (under the `run` member function). The following is a very basic example of a [Task](tests/tasks/task.py):

```python
class Task(tasks.BaseTask):
    def run(self):
        return {"key": "value"}
```

Since the framework is asynchronous, once the `Task` finishes its execution, the results will be stored in a given location. For each storage location, a [BaseStorage](dragonscales/storages.py) subclass must be created. The `store` member function writes the results in a certain location, and return its path. Again, the following is the most basic example of a [Storage](tests/storages/storage.py):

```python
class Storage(storages.BaseStorage):
    def store(self, result):
        storage_path = "/tmp/dragonscale.storage"
        with open(storage_path, "w") as storage_file:
            storage_file.write(json.dumps(result))
        return {"path": storage_path}
```

Lastly, the callback is in charge of returning the results' location to the client. For each callback path desired, a subclass of [BaseCallback](dragonscales/callbacks.py) must be created. The member function `call` then writes the storage location into the callback location. And once a again, a basic  [Callback](tests/callbacks/callback.py) example is shown below.

```python
class Callback(callbacks.BaseCallback):
    def call(self, location):
        callback_path = "/tmp/dragonscale.callback"
        with open(callback_path, "w") as callback_file:
            callback_file.write(json.dumps(location))

```

If you decide you want to add some authorization logic for the clients to access the service, you should implement a [BaseAuthorizer](dragonscales/authorizers.py) subclass.

---

Once you're done with all the previous implementation, there is only one thing left to do: "feed" `dragonscales` with your tasks, storages, callbacks, and authorizer, along with the path to their respective modules and required parameters. You also need to list the names of all the queues that will be available in the jobs system.

The path to the JSON project file must be exported with the environment variable `DRAGONSCALES_PROJECT_PATH`. A basic example of a project file can be found in [here](tests/projects/test.json).

### Service client

Once the service is up and running (see installation and setup instructions below), the clients can run a task very easily by requesting the service to queue a job for that task. All they need to do is use the API to specify the task, the storage, and the callback desired - each one defined by its name and parameters. As an example, they can create a job with the following JSON:

```json
{
  "task": {
    "name": "task",
    "params": {}
  },
  "storage": {
    "name": "storage",
    "params": {}
  },
  "callback": {
    "name": "callback",
    "params": {}
  }
}

```

---

<p align="center">
    <img width="70%" src="./data/diagram.svg"><br>
    Figure 1: <em>The interaction of both the developer and the client with the framework.</em>
</p>


## Installation

```bash
$ sudo apt install virtualenv redis
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

## Setup

```bash
$ cp tests/projects/test.json project.json
$ vim project.json # personalize it!
```

## Running the service

On parallel tabs, run:

```bash
$ redis-server
```

For each queue in specified in the JSON project file, run a worker in a different tab.
```bash
$ rq worker $QUEUE
```

```bash
$ export DRAGONSCALES_PROJECT_PATH=project.json
$ export DRAGONSCALES_REDIS_URL=redis://localhost:6379
$ gunicorn --bind 0.0.0.0:5003 --worker-class=uvicorn.workers.UvicornWorker wsgi-dragonscales:app
```
