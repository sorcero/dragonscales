# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Sorcero, Inc.
#
# This file is part of Sorcero's Language Intelligence platform
# (see https://www.sorcero.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from typing import List
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .engines import Engine
from .schemas import JobStatus

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
def create(
    request: engine.get_job_request_schema(), user: dict = Depends(engine.authorize)
):
    job = engine.enqueue(request.task, request.storage, request.callback)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result={})


@app.get("/api/v1/jobs/{id}", response_model=JobStatus)
def get(id: str, user: dict = Depends(engine.authorize)):
    job = engine.fetch(id)
    return JobStatus(id=job.id, status=job.get_status(refresh=True), result=job.result)


@app.get("/api/v1/jobs/", response_model=List[str])
def list(user: dict = Depends(engine.authorize)):
    return engine.get_jobs()


@app.delete("/api/v1/jobs/{id}", response_model=None)
def cancel(id: str, user: dict = Depends(engine.authorize)):
    engine.cancel(id)
