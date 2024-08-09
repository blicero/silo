#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-09 18:56:05 krylon>
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
class Record:
    """Record represents a single log record."""

    record_id: int
    host_id: int
    timestamp: datetime
    source: str
    message: str


# Local Variables: #
# python-indent: 4 #
# End: #
