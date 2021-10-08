from fastapi import FastAPI
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
def create(request: JobRequest):
    job = engine.enqueue(request.task)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result={})


@app.get("/api/v1/jobs/{id}", response_model=JobStatus)
def get(id: str):
    job = engine.fetch(id)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result=job.result)
