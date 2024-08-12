#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 18:00:49 krylon>
#
# /data/code/python/silo/test_database.py
# created on 10. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.test_database

(c) 2024 Benjamin Walkenhorst
"""

import os
import sqlite3
import unittest
from datetime import datetime

from krylib import isdir

from silo import common, database
from silo.data import Host, Record

TEST_ROOT: str = "/tmp"

# On my main development machines, I have a RAM disk mounted at /data/ram.
# If it's available, I'd rather use that than /tmp which might live on disk.
if isdir("/data/ram"):
    TEST_ROOT = "/data/ram"


class DatbaseTest(unittest.TestCase):
    """Test the database."""

    folder: str
    db: database.Database

    @classmethod
    def setUpClass(cls) -> None:  # noqa: D102
        stamp = datetime.now()
        folder_name = \
            stamp.strftime("silo_test_database_%Y%m%d_%H%M%S")
        cls.folder = os.path.join(TEST_ROOT,
                                  folder_name)
        common.set_basedir(cls.folder)

    @classmethod
    def tearDownClass(cls) -> None:  # noqa: D102
        os.system(f"/bin/rm -rf {cls.folder}")

    def __get_db(self) -> database.Database:
        """Get the shared database instance."""
        return self.__class__.db

    def test_01_db_open(self) -> None:
        """Test opening a new database."""
        try:
            self.__class__.db = database.Database(common.path.db())
        except Exception as e:  # pylint: disable-msg=W0718
            self.fail(f"Failed to open database: {e}")
        finally:
            self.assertIsNotNone(self.__class__.db)

    def test_02_host_add(self) -> None:
        """Test adding Hosts."""
        test_cases = [
            (Host(name="host01"), False),
            (Host(name="host02"), False),
            (Host(name="host03"), False),
            (Host(name="host01"), True),
        ]

        db = self.__get_db()
        for c in test_cases:
            if c[1]:
                with self.assertRaises(sqlite3.IntegrityError):
                    db.host_add(c[0])
            else:
                try:
                    db.host_add(c[0])
                except Exception as ex:  # pylint: disable-msg=W0718
                    self.fail(f"Failed to add Host {c[0].name} to database: {ex}")
                else:
                    self.assertNotEqual(c[0].host_id, 0)

    def test_03_host_get(self) -> None:
        """Test fetching the hosts we just added"""
        db = self.__get_db()
        hosts = db.host_get_all()
        self.assertIsNotNone(hosts)
        self.assertEqual(len(hosts), 3)
        for h in hosts:
            self.assertIsInstance(h, Host)

    def test_04_record_add(self) -> None:
        """Test adding log records."""
        test_cases: list[tuple[Record, bool]] = [
            (Record(
                host_id=1,
                timestamp=datetime.fromtimestamp(10),
                source="kernel",
                message="Test 01"), False),
            (Record(
                host_id=1,
                timestamp=datetime.fromtimestamp(20),
                source="kernel",
                message="Test 02"), False),
        ]

        db = self.__get_db()

        for c in test_cases:
            try:
                db.record_add(c[0])
            except Exception as err:  # pylint: disable-msg=W0718
                self.fail(f"Error adding record {c[0].message}: {err}")
            else:
                self.assertNotEqual(c[0].record_id, 0)

# Local Variables: #
# python-indent: 4 #
# End: #
