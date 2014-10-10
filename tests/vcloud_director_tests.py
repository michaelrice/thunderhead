# Copyright 2014 Zaheena Kashif
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

import vcr

from thunderhead.connection import Connection

import tests
from thunderhead.builder import vcloud_director


class VcloudDirectorTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_all_vcd_not_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_all_vcd(self):
        with self.assertRaises(vcloud_director.VcdNotFoundException):
            vcloud_director.get_all_vcd(tests.CONNECTION)

    @vcr.use_cassette('create_vcd_fail.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_vcd_fail(self):
        vcd_info = {
            'hostname': '172.16.214.131',
            'username': 'root',
            'password': 'vmware'
        }
        vcd = vcloud_director.create_vcd_server(tests.CONNECTION, vcd_info)
        self.assertIsInstance(vcd, dict)

    @vcr.use_cassette('create_vcd.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_vcd(self):
        vcd_info = {
            'hostname': '',
            'username': '',
            'password': ''
        }
        vcd = vcloud_director.create_vcd_server(tests.CONNECTION, vcd_info)
        self.assertIsInstance(vcd, dict)

