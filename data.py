#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-10 21:22:35 krylon>
#
# /data/code/python/silo/data.py
# created on 09. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.data

(c) 2024 Benjamin Walkenhorst
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, kw_only=True)
class Host:
    """Host represents a Host on the network."""

    host_id: int = 0
    name: str


@dataclass(slots=True, kw_only=True)
class Record:
    """Record represents a single log record."""

    record_id: int = 0
    host_id: int = 0
    timestamp: datetime
    source: str
    message: str


# Local Variables: #
# python-indent: 4 #
# End: #
