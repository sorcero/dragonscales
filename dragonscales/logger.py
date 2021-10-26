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
import logging
import json_logging

DRAGONSCALES_LOGGER_LEVEL = os.environ.get("DRAGONSCALES_LOGGER_LEVEL", "INFO")
DRAGONSCALES_LOGGER_PATH = os.environ.get("DRAGONSCALES_LOGGER_PATH", None)
DRAGONSCALES_LOGGER_MAX_BYTES = int(os.environ.get("DRAGONSCALES_LOGGER_MAX_BYTES", 0))

json_logging.init_fastapi(enable_json=True)

logger = logging.getLogger("dragonscales")
logger.setLevel(level=getattr(logging, DRAGONSCALES_LOGGER_LEVEL))

if DRAGONSCALES_LOGGER_PATH is not None:
    logger.addHandler(
        logging.handlers.RotatingFileHandler(
            DRAGONSCALES_LOGGER_PATH, maxBytes=DRAGONSCALES_LOGGER_MAX_BYTES
        )
    )
else:
    logger.addHandler(logging.StreamHandler())
