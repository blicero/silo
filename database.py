#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-10 22:16:47 krylon>
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

import logging
import sqlite3
from enum import Enum, auto
from threading import Lock
from typing import Final

import krylib

from silo import common

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


db_queries: Final[dict[QueryID, str]] = {
    QueryID.HostAdd: "INSERT INTO host (name) VALUES (?) RETURNING id",
    QueryID.HostGetByName: "SELECT id, last_contact FROM host WHERE name = ?",
    QueryID.HostGetAll: "SELECT id, name, last_contact FROM host",
    QueryID.HostUpdateLastContact: "UPDATE host SET last_contact = ? WHERE id = ?",
    QueryID.RecordAdd: """
    INSERT INTO record (host_id, timestamp, source, message)
                VALUES (      ?,         ?,      ?,       ?)
    RETURNING id""",
    QueryID.RecordGetByHost: "SELECT id, timestamp, source, message FROM record WHERE host_id = ?",
    QueryID.RecordGetByPeriod: """
    SELECT
        id,
        host_id,
        timestamp,
        source,
        message
    FROM record
    WHERE timestamp BETWEEN ? AND ?
    """,
}


class Database:
    """Database provides persistence."""

    __slots__ = [
        "db",
        "log",
        "path",
    ]

    db: sqlite3.Connection
    log: logging.Logger
    path: Final[str]

    def __init__(self, path: str = "") -> None:
        if path == "":
            path = common.path.db()
        self.log = common.get_logger("database")
        self.log.debug("Open database at %s", path)
        with OpenLock:
            exist: bool = krylib.fexist(path)
            self.db = sqlite3.connect(path)  # pylint: disable-msg=C0103
            self.db.isolation_level = None

            cur: sqlite3.Cursor = self.db.cursor()
            cur.execute("PRAGMA foreign_keys = true")
            cur.execute("PRAGMA journal_mode = WAL")

            if not exist:
                self.__create_db()

    def __create_db(self) -> None:
        """Initialize a newly created database."""
        with self.db:
            for query in InitQueries:
                cur: sqlite3.Cursor = self.db.cursor()
                cur.execute(query)

    def __enter__(self) -> None:
        self.db.__enter__()

    def __exit__(self, ex_type, ex_val, traceback):
        return self.db.__exit__(ex_type, ex_val, traceback)

# Local Variables: #
# python-indent: 4 #
# End: #
