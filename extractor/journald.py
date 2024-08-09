#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-09 21:40:46 krylon>
#
# /data/code/python/silo/extractor/journald.py
# created on 09. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.extractor.journald

(c) 2024 Benjamin Walkenhorst
"""

from systemd.journal import Reader

from silo.extractor.base import BaseExtractor
from silo.data import Record


class JournaldExtractor(BaseExtractor):
    """JournaldExtractor reads journald log files."""

    __slots__ = [
        "rdr",
    ]

    rdr: Reader

    def __init__(self) -> None:
        self.rdr = Reader()

    def init(self) -> None:
        pass

    def read_next(self) -> Record:
        raw = self.rdr.get_next()
        rec = Record(
            timestamp=raw["__REALTIME_TIMESTAMP"],
            message=raw["MESSAGE"],
            source=raw["_COMM"],
        )

        return rec

# Local Variables: #
# python-indent: 4 #
# End: #
