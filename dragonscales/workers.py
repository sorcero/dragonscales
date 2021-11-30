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

import os

from rq import Queue, get_current_job
from .schemas import JobStatus, Status

from .logger import logger


def deliver_success(job, connection, result, *args, **kargs):
    enqueue_delivery(job, connection)


def deliver_failure(job, connection, type, value, traceback):
    enqueue_delivery(job, connection)


def enqueue_delivery(job, connection):
    queue = Queue(
        os.environ.get("DRAGONSCALES_DELIVERY_QUEUE_NAME", "delivery"),
        connection=connection,
    )
    queue.enqueue(deliver_results, job.id, meta=job.meta)


def deliver_results(job_id):
    delivery_job = get_current_job()

    queue = Queue(delivery_job.meta["queue"], connection=delivery_job.connection)

    job = queue.fetch_job(job_id)
    job_status = Status.get(job.get_status(refresh=True))

    logger.debug(
        "delivering", extra={"props": {"job_id": job.id, "status": job_status}}
    )

    status = JobStatus(
        id=job.id,
        status=job_status,
        result=job.result,
        info=job.exc_info,
    )

    callback = job.meta["callback"]
    callback_params = job.meta["callback_params"]
    callback.call(status.dict(), **callback_params)
