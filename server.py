#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 21:42:53 krylon>
#
# /data/code/python/silo/server.py
# created on 12. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.server

(c) 2024 Benjamin Walkenhorst
"""

import logging
from socketserver import ThreadingTCPServer
from threading import local

from silo import common


class Server(ThreadingTCPServer):
    """Server serves the Agents and the Frontend."""

    log: logging.Logger
    pool: local

    def __init__(self, *_args, **_kwargs) -> None:
        super().__init__(*_args, **_kwargs)
        self.log = common.get_logger("server")
        self.pool = local()

# Local Variables: #
# python-indent: 4 #
# End: #
