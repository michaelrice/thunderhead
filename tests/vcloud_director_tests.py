# Copyright 2014 Zaheena Kashif, Michael Rice
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

import tests
from thunderhead.builder import vcloud_director


class VcloudDirectorTests(tests.VCRBasedTests):

    @vcr.use_cassette('create_vcd_success.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_vcd_success(self):
        vcd_info = {
            'hostname': '10.12.254.111',
            'username': 'administrator',
            'password': 'password'
        }
        vcd = vcloud_director.create_vcd_server(tests.CONNECTION, vcd_info)
        self.assertIsInstance(vcd, dict)

