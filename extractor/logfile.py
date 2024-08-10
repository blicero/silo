#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-11 01:21:54 krylon>
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

from silo.extractor.base import BaseExtractor


class LogfileExtractor(BaseExtractor):
    """SyslogExtractor reads from good old-fashioned log files."""

    __slots__ = [
        "files",
        "handles",
    ]

    files: list[str]
    handles: list[io.TextIOBase]

    def __init__(self, *files: str) -> None:
        self.files = list(files)
        self.handles = []

    def init(self) -> None:
        """Open the log file(s)."""
        handles: list[io.TextIOBase] = []
        for f in self.files:
            fh = open(f, "r", encoding="utf-8")  # pylint: disable-msg=R1732
            handles.append(fh)
        self.handles = handles

# Local Variables: #
# python-indent: 4 #
# End: #
