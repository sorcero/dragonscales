from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .engines import Engine
from .schemas import JobRequest, JobStatus

engine = Engine()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/jobs/", response_model=JobStatus)
def create(request: JobRequest, user: dict = Depends(engine.authorize)):
    job = engine.enqueue(request.task, request.storage, request.callback)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result={})


@app.get("/api/v1/jobs/{id}", response_model=JobStatus)
def get(id: str, user: dict = Depends(engine.authorize)):
    job = engine.fetch(id)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result=job.result)


@app.get("/api/v1/jobs/", response_model=List[str])
def list(user: dict = Depends(engine.authorize)):
    return engine.get_jobs()


@app.delete("/api/v1/jobs/{id}", response_model=JobStatus)
def cancel(id: str, user: dict = Depends(engine.authorize)):
    job = engine.cancel(id)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result=job.result)
