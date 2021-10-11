# dragonscales

![Basic Concepts](./data/diagram.svg)

## Installation

```
$ sudo apt install virtualenv redis
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

## Setup

```
$ cp tests/projects/test.json project.json
$ vim project.json # personalize it !
```

## Run

```
$ export DRAGONSCALES_PROJECT_PATH=project.json
$ export DRAGONSCALES_REDIS_URL=redis://localhost:6379
$ redis-server
$ gunicorn --bind 0.0.0.0:5003 --worker-class=uvicorn.workers.UvicornWorker wsgi-dragonscales:app
$ rq worker $QUEUE
```

Note that workers can listen to different `$QUEUE`, defined in `project.json`.
