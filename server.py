#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-13 20:18:51 krylon>
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

from socketserver import StreamRequestHandler, ThreadingTCPServer

from silo.database import Database, DBPool


class RequestHandler(StreamRequestHandler):
    """RequestHandler implements the actual protocol."""

    pool = DBPool()

    def handle(self) -> None:
        data = self.request[0].strip()


# Local Variables: #
# python-indent: 4 #
# End: #
