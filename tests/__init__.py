# Copyright 2014 Michael Rice <michael@michaelrice.org>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import logging
import os
import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from thunderhead.connection import Connection

ADMIN_TOKEN = "TOKSDVLMROYMFIYEDBLHXDHLPIV5IDYGHM2"
USER_TOKEN = "TOKFWZWF5TO34NUREN5KETI2B1KESAC3HRZ"
CONNECTION = Connection(host='vusagemeter',
                        token=ADMIN_TOKEN)


def tests_resource_path(local_path=''):
    this_file = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_file, local_path)

# Full path to the fixtures directory underneath this module
fixtures_path = tests_resource_path(local_path='fixtures')


class ThunderheadTests(unittest.TestCase):
    pass


class VCRBasedTests(unittest.TestCase):
    def setUp(self):
        logging.basicConfig()
        vcr_log = logging.getLogger('vcr')
        vcr_log.setLevel(logging.DEBUG)