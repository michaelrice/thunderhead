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

import tests
from thunderhead.connection import Connection
from thunderhead.builder import customers


class CustomerTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_all_customers.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_all_customers(self):
        connection = Connection(host='vusagemeter',
                                token=tests.ADMIN_TOKEN,
                                )
        usage_customers = customers.get_all_customers(connection)
        self.assertEquals(isinstance(usage_customers, list), True)
        self.assertEquals(len(usage_customers), 3)

    @vcr.use_cassette('get_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_single_customer(self):
        connection = Connection(host='vusagemeter',
                                token=tests.ADMIN_TOKEN,
                                )
        usage_customer = customers.get_customer(connection, 1)
        c1_dict = {'country': 'United States', 'customer_id': '1',
                   'postal_code': '78232', 'name': '1018700'}
        self.assertDictEqual(usage_customer, c1_dict)