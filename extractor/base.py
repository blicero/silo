#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 18:18:25 krylon>
#
# /data/code/python/silo/extractor/base.py
# created on 09. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.base

(c) 2024 Benjamin Walkenhorst
"""

from abc import ABC, abstractmethod
from datetime import datetime

from silo.data import Record


class BaseExtractor(ABC):
    """Abstract base class for log extractors."""

    @abstractmethod
    def init(self) -> None:
        """Open the log."""

    @abstractmethod
    def read(self, begin: datetime) -> list[Record]:
        """Read the log."""

    @abstractmethod
    def close(self) -> None:
        """Close the log."""

# Local Variables: #
# python-indent: 4 #
# End: #
