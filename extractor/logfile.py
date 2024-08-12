#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 19:39:35 krylon>
#
# /data/code/python/silo/extractor/logfile.py
# created on 11. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.extractor.syslog

(c) 2024 Benjamin Walkenhorst
"""

import io
import re
from datetime import datetime
from typing import Final

from dateutil import parser

from silo.data import Record
from silo.extractor.base import BaseExtractor

line_pat: Final[re.Pattern] = re.compile(
    r"""^(\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2}) \s+ # timestamp
    (\w+) \s+ # hostname
    (\w+)(?:\[\d+\])?: \s+ # source
    (.*)$""",
    re.I | re.X)


class LogfileExtractor(BaseExtractor):
    """SyslogExtractor reads from good old-fashioned log files."""

    __slots__ = [
        "files",
        "handles",
    ]

    files: list[str]
    handles: list[io.TextIOBase]

    def __init__(self, *files: str) -> None:
        super().__init__()
        self.files = list(files)
        self.handles = []

    def init(self) -> None:
        """Open the log file(s)."""
        handles: list[io.TextIOBase] = []
        for f in self.files:
            fh = open(f, "r", encoding="utf-8")  # pylint: disable-msg=R1732
            handles.append(fh)
        self.handles = handles

    def read(self, begin: datetime) -> list[Record]:
        """Read the log."""
        records: list[Record] = []
        for h in self.handles:
            for line in h:
                m = line_pat.match(line.rstrip("\n"))
                if m is None:
                    continue
                timestamp, _, source, message = m.groups()
                r: Record = Record(
                    timestamp=parser.parse(timestamp),
                    source=source,
                    message=message)
                records.append(r)
        return records

# Local Variables: #
# python-indent: 4 #
# End: #
