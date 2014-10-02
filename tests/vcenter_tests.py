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

import vcr

from thunderhead.connection import Connection

import tests
from thunderhead.builder import vcenter


class VcenterTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_all_vcenters_not_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_all_vcenters_not_found(self):
        with self.assertRaises(vcenter.VCenterException):
            vcenter.get_all_vcenters(tests.CONNECTION)

    @vcr.use_cassette('get_all_vcenters_no_route_to_host.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_all_vcenters_no_route_to_host(self):
        bad_connection = Connection(host="null", token="bad")
        with self.assertRaises(vcenter.VCenterException):
            vcenter.get_all_vcenters(bad_connection)

    @vcr.use_cassette('get_all_vcenters.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_all_vcenters(self):
        vcenters = vcenter.get_all_vcenters(tests.CONNECTION)
        self.assertIsNotNone(vcenters)
        self.assertIsInstance(vcenters, list)
        d1 = {
            'username': 'root',
            'instanceUuid': '137E2125-73EB-4E1B-BF03-2B6CD396E6AC',
            'monitor': 'false',
            'hostname': '172.16.214.129',
            'meter': 'true',
            'version': '5.5.0',
            'active': 'true',
            'fullname': 'VMware vCenter Server 5.5.0 build-1945287 (Sim)',
            'id': '1'
        }
        self.assertDictEqual(d1, vcenters[0])

    @vcr.use_cassette('get_vcenter_by_id_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_vcenter_by_id_found(self):
        vc = vcenter.get_vcenter(tests.CONNECTION, 1)
        d1 = {
            'username': 'root',
            'instanceUuid': '137E2125-73EB-4E1B-BF03-2B6CD396E6AC',
            'monitor': 'false',
            'hostname': '172.16.214.129',
            'meter': 'true',
            'version': '5.5.0',
            'active': 'true',
            'fullname': 'VMware vCenter Server 5.5.0 build-1945287 (Sim)',
            'id': '1'
        }
        self.assertIsNotNone(vc)
        self.assertIsInstance(vc, dict)
        self.assertDictEqual(d1, vc)

    @vcr.use_cassette('get_vcenter_by_id_not_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_vcenter_by_id_not_found(self):
        with self.assertRaises(vcenter.VCenterException):
            vcenter.get_vcenter(tests.CONNECTION, 1000)

    # TODO: come back to fix when bug addressed.
    @vcr.use_cassette('create_vcenter.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_vcenter(self):
        vc_info = {
            'hostname': '172.16.214.131',
            'username': 'root',
            'password': 'vmware',
            'monitor': 'true'
        }
        vc = vcenter.create_vcenter(tests.CONNECTION, vc_info)
        self.assertIsInstance(vc, dict)

    @vcr.use_cassette('delete_vcenter.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_update_vcenter(self):
        pass

    @vcr.use_cassette('update_vcenter.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_delete_vcenter(self):
        pass
