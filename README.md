# dragonscales :dragon:

`dragonscales` is a highly customizable asynchronous job-scheduler framework. This framework is used to scale the execution of multiple tasks by multiple clients. A developer can expose several predefined tasks that are available to the clients through a jobs service, without the need to build the job system itself.

## Usage

<p align="center">
    <img width="70%" src="./data/diagram.svg"><br>
    Figure 1: <em>The interaction of both the developer and the client with the framework.</em>
</p>

### Service developer

As the developer, you need to populate the service with the tasks that will later be available for the clients to run.

For each task you want to expose, a [BaseTask](dragonscales/tasks.py) subclass needs to be created. The `run` method is invoked to execute the task. The following is a basic example of a [Task](tests/tasks/task.py):

```python
class Task(tasks.BaseTask):
    def run(self):
        return {"key": "value"}
```

Once the `Task` finishes its execution, the results will be stored in a given location. For each storage location, a [BaseStorage](dragonscales/storages.py) subclass must be created. The `store` method writes the results in a certain location, and returns its location information. Again, the following is a basic example of a [Storage](tests/storages/storage.py):

```python
class Storage(storages.BaseStorage):
    def store(self, result):
        storage_path = "/tmp/dragonscale.storage"
        with open(storage_path, "w") as storage_file:
            storage_file.write(json.dumps(result))
        return {"path": storage_path}
```

Since the framework is asynchronous, the callback is in charge of returning the results' location to the client. For each callback method, a subclass of [BaseCallback](dragonscales/callbacks.py) must be created. The `call` method sends the location information to the client. And once a again, a basic [Callback](tests/callbacks/callback.py) example is shown below.

```python
class Callback(callbacks.BaseCallback):
    def call(self, location):
        callback_path = "/tmp/dragonscale.callback"
        with open(callback_path, "w") as callback_file:
            callback_file.write(json.dumps(location))

```

If you decide you want to add some authorization step for the clients to access the service, you must implement a [BaseAuthorizer](dragonscales/authorizers.py) subclass. See this basic [Authorizer](tests/authorizers/authorizer.py) example.

---

Once you're done with all the previous implementation steps, there is only one thing left to do: Create a `dragonscales` project file with your tasks, storages, callbacks, and authorizer, along with the path to their respective modules and constructor arguments. You also need to list the names of all the queues that will be available in the jobs system.

The path to the project file must be exported with the environment variable `DRAGONSCALES_PROJECT_PATH`. A basic example of a project file can be found in [here](tests/projects/test.json).

### Service client

Once the service is up and running (see installation and setup instructions below), the clients can run a task by requesting the service to queue a job for that task. The client invokes the `/api/v1/jobs` endpoint to specify a specific task, storage, and callback among the available ones - each one defined by its name and parameters. See this [job request](tests/jobs/test.json) as an example.

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
