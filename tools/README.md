# Tools

## dragonscales-manager

### Queue a job

```
$ dragonscales-manager \
    --url http://localhost:5003 \
    queue ../tests/jobs/test.json
```

### Check job status

```
$ dragonscales-manager \
    --url http://localhost:5003 \
    check XXX
    --wait
```

### Remove a job

```
$ dragonscales-manager \
    --url http://localhost:5003 \
    remove XXX
```

### List jobs

```
$ dragonscales-manager \
    --url http://localhost:5003 \
    list
```

### Set headers

```
$ dragonscales-manager \
    --header X-API-Key YYY \
    --header correlation-id ZZZ \
    --url http://localhost:5003 \
    list
```
