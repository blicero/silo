#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 17:51:57 krylon>
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
from datetime import datetime
from enum import Enum, auto
from threading import Lock
from typing import Final, Optional

import krylib

from silo import common
from silo.data import Host, Record

InitQueries: Final[list[str]] = [
    """
    CREATE TABLE host (
        id              INTEGER PRIMARY KEY,
        name            TEXT UNIQUE NOT NULL,
        last_contact    INTEGER NOT NULL DEFAULT 0
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
    HostGetByID = auto()
    HostGetAll = auto()
    HostUpdateLastContact = auto()
    RecordAdd = auto()
    RecordGetByHost = auto()
    RecordGetByPeriod = auto()


db_queries: Final[dict[QueryID, str]] = {
    QueryID.HostAdd: "INSERT INTO host (name) VALUES (?) RETURNING id",
    QueryID.HostGetByName: "SELECT id, last_contact FROM host WHERE name = ?",
    QueryID.HostGetByID: "SELECT name, last_contact FROM host WHERE id = ?",
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
    path: str

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
                try:
                    cur: sqlite3.Cursor = self.db.cursor()
                    cur.execute(query)
                except sqlite3.OperationalError as err:
                    self.log.error("Error executing init query: %s\n%s\n",
                                   err,
                                   query)
                    raise

    def __enter__(self) -> None:
        """Begin a transaction."""
        self.db.__enter__()

    def __exit__(self, ex_type, ex_val, traceback):
        """Finish a transaction."""
        return self.db.__exit__(ex_type, ex_val, traceback)

    def host_add(self, host: Host) -> None:
        """Add a Host to the database."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.HostAdd],
                    (host.name, ))
        row = cur.fetchone()
        host.host_id = row[0]

    def host_get_by_name(self, name: str) -> Optional[Host]:
        """Fetch a Host by its name."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.HostGetByName],
                    (name, ))
        row = cur.fetchone()
        if row is not None:
            return Host(host_id=row[0],
                        name=name,
                        last_contact=datetime.fromtimestamp(row[1]))
        self.log.debug("Host %s was not found in database.", name)
        return None

    def host_get_by_id(self, hid: int) -> Optional[Host]:
        """Fetch a Host by its database ID."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.HostGetByID], (hid, ))
        row = cur.fetchone()
        if row is not None:
            return Host(host_id=hid,
                        name=row[0],
                        last_contact=datetime.fromtimestamp(row[1]))
        self.log.debug("No Host with ID %d was found in database.", hid)
        return None

    def host_get_all(self) -> list[Host]:
        """Fetch all Hosts from the database."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.HostGetAll])
        hosts: list[Host] = []
        for row in cur:
            h: Host = Host(
                host_id=row[0],
                name=row[1],
                last_contact=datetime.fromtimestamp(row[2]),
            )
            hosts.append(h)
        return hosts

    def host_update_contact(self, h: Host) -> None:
        """Update a Host's contact timestamp."""
        stamp: datetime = datetime.now()
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.HostUpdateLastContact],
                    (int(stamp.timestamp()), h.host_id))
        h.last_contact = stamp

    def record_add(self, rec: Record) -> None:
        """Add a log record to the database."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.RecordAdd],
                    (rec.host_id, int(rec.timestamp.timestamp()), rec.source, rec.message))
        row = cur.fetchone()
        rec.record_id = row[0]

    def record_get_by_host(self, host: int) -> list[Record]:
        """Fetch all log records for the given Host."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.RecordGetByHost], (host, ))
        results: list[Record] = []
        for row in cur:
            rec = Record(record_id=row[0],
                         host_id=host,
                         timestamp=datetime.fromtimestamp(row[1]),
                         source=row[2],
                         message=row[3])
            results.append(rec)
        return results

    def record_get_by_period(self, begin: datetime, end: datetime) -> list[Record]:
        """Fetch all Records for the given period."""
        cur: sqlite3.Cursor = self.db.cursor()
        cur.execute(db_queries[QueryID.RecordGetByPeriod],
                    (int(begin.timestamp()), int(end.timestamp())))
        results: list[Record] = []
        for row in cur:
            rec: Record = Record(record_id=row[0],
                                 host_id=row[1],
                                 timestamp=datetime.fromtimestamp(row[2]),
                                 source=row[3],
                                 message=row[4])
            results.append(rec)
        return results

# Local Variables: #
# python-indent: 4 #
# End: #
