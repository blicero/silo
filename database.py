#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-10 21:43:10 krylon>
#
# /data/code/python/silo/database.py
# created on 10. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.database

(c) 2024 Benjamin Walkenhorst
"""

from enum import Enum, auto
from threading import Lock
from typing import Final

InitQueries: Final[list[str]] = [
    """
    CREATE TABLE host (
        id              INTEGER PRIMARY KEY,
        name            TEXT UNIQUE NOT NULL,
        last_contact    INTEGER NOT NULL DEFAULT 0,
    ) STRICT
    """,
    "CREATE UNIQUE INDEX host_name_idx ON host (name)",
    """
    CREATE TABLE record (
        id              INTEGER PRIMARY KEY,
        host_id         INTEGER NOT NULL,
        timestamp       INTEGER NOT NULL,
        source          TEXT NOT NULL,
        message         TEXT NOT NULL,
        FOREIGN KEY (host_id) REFERENCES host (id)
                ON DELETE CASCADE
                ON UPDATE RESTRICT
    ) STRICT
    """,
    "CREATE INDEX record_host_idx ON record (host_id)",
    "CREATE INDEX record_time_idx ON record (timestamp)",
]

OpenLock: Final[Lock] = Lock()


class QueryID(Enum):
    """QueryID identifies database queries."""

    HostAdd = auto()
    HostGetByName = auto()
    HostGetAll = auto()
    HostUpdateLastContact = auto()
    RecordAdd = auto()
    RecordGetByHost = auto()
    RecordGetByPeriod = auto()


# Local Variables: #
# python-indent: 4 #
# End: #
