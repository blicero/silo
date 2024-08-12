#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time-stamp: <2024-08-12 20:13:17 krylon>
#
# /data/code/python/silo/extractor/test_syslog.py
# created on 12. 08. 2024
# (c) 2024 Benjamin Walkenhorst
#
# This file is part of the Vox audiobook reader. It is distributed under the
# terms of the GNU General Public License 3. See the file LICENSE for details
# or find a copy online at https://www.gnu.org/licenses/gpl-3.0

"""
silo.extractor.test_syslog

(c) 2024 Benjamin Walkenhorst
"""

import unittest
from typing import Final

from silo.extractor.logfile import line_pat

# noqa: E501
test_content: Final[str] = """
Aug  9 00:00:00 wintermute newsyslog[8927]: logfile turned over due to size>1000K
Aug  9 00:00:04 wintermute named[951]: success resolving '3.f.9.f.0.4.6.6.b.a.9.b.3.3.e.f.0.0.a.0.2.0.7.1.1.4.8.4.0.0.a.2.ip6.arpa/PTR' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:00:04 wintermute named[951]: success resolving '6.0.5.4.5.d.7.1.a.6.f.4.5.3.d.9.0.0.a.0.2.0.7.1.1.4.8.4.0.0.a.2.ip6.arpa/PTR' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:00:04 wintermute named[951]: success resolving '5.0.8.6.a.8.0.b.1.b.5.3.1.f.1.4.0.0.a.0.2.0.7.1.1.4.8.4.0.0.a.2.ip6.arpa/PTR' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:00:04 wintermute named[951]: success resolving '6.9.5.1.b.f.7.b.0.2.3.9.8.a.8.6.0.0.a.0.2.0.7.1.1.4.8.4.0.0.a.2.ip6.arpa/PTR' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:01:10 wintermute named[951]: success resolving 'puffball.us-east.host.bsky.network/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:02:24 wintermute smartd[2488]: Device: /dev/ada0, SMART Usage Attribute: 194 Temperature_Celsius changed from 115 to 116
Aug  9 00:02:24 wintermute smartd[2488]: Device: /dev/ada1, SMART Usage Attribute: 194 Temperature_Celsius changed from 114 to 115
Aug  9 00:04:31 wintermute named[951]: validating omny.fm/A: no valid signature found
Aug  9 00:04:31 wintermute named[951]: validating omny.fm/AAAA: no valid signature found
Aug  9 00:06:05 wintermute named[951]: clients-per-query increased to 17
Aug  9 00:06:31 wintermute named[951]: success resolving 'star-mini.c10r.facebook.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:06:31 wintermute named[951]: success resolving 'star-mini.c10r.facebook.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.nccp.dradis.netflix.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.nccp.dradis.netflix.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.prod.dradis.netflix.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.prod.dradis.netflix.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.prod.eu-west-1.internal.dradis.netflix.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'api-global.eu-west-1.internal.dradis.netflix.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'api-global.eu-west-1.internal.dradis.netflix.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'uiboot.eu-west-1.internal.dradis.netflix.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'uiboot.eu-west-1.internal.dradis.netflix.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:07:58 wintermute named[951]: success resolving 'nrdp.prod.eu-west-1.internal.dradis.netflix.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:08:00 wintermute named[951]: success resolving 'ocsp.rootca1.amazontrust.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:08:00 wintermute named[951]: success resolving 'ocsp.rootca1.amazontrust.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:08:00 wintermute named[951]: success resolving 'ocsp.r2m03.amazontrust.com/AAAA' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:08:00 wintermute named[951]: success resolving 'ocsp.r2m03.amazontrust.com/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:09:35 wintermute named[951]: validating omny.fm/A: no valid signature found
Aug  9 00:09:35 wintermute named[951]: validating omny.fm/AAAA: no valid signature found
Aug  9 00:11:10 wintermute named[951]: success resolving 'puffball.us-east.host.bsky.network/A' after disabling qname minimization due to 'ncache nxdomain'
Aug  9 00:14:36 wintermute named[951]: validating omny.fm/A: no valid signature found
Aug  9 00:14:36 wintermute named[951]: validating omny.fm/AAAA: no valid signature found
Aug  9 00:16:10 wintermute named[951]: success resolving 'puffball.us-east.host.bsky.network/A' after disabling qname minimization due to 'ncache nxdomain'
"""


class SyslogTest(unittest.TestCase):
    """Test the syslog reader"""

    def test_parse_line(self) -> None:
        """Test parsing lines."""
        for line in test_content.split("\n"):
            if line == "":
                continue
            m = line_pat.match(line)
            self.assertIsNotNone(m, msg=f"Failed to parse line: {line}")

# Local Variables: #
# python-indent: 4 #
# End: #
