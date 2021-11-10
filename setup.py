#!/usr/bin/env python
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

from setuptools import setup

setup(
    name="dragonscales",
    version="0.1.0",
    description="A highly-customizable asynchronous job-scheduler framework",
    author="Sorcero, Inc.",
    author_email="dragonscales@sorcero.com",
    url="https://gitlab.com/sorcero/community/dragonscales",
    packages=["dragonscales"],
    license="LGPL-3.0-or-later",
    license_files = ("LICENSE",),
    scripts=["tools/dragonscales-manager"],
    install_requires=[
        "click==7.1.2",
        "uvicorn==0.11.7",
        "fastapi==0.60.0",
        "gunicorn==20.0.4",
        "redis==3.5.3",
        "rq==1.8.1",
        "black==21.9b0",
        "pyflakes==2.4.0",
        "pytest==6.2.5",
        "requests==2.26.0",
        "json-logging==1.3.0",
    ]
)
