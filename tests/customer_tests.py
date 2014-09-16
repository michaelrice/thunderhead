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
from thunderhead.builder import customers


class CustomerTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_all_customers.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_all_customers(self):
        usage_customers = customers.get_all_customers(tests.CONNECTION)
        self.assertEquals(isinstance(usage_customers, list), True)
        self.assertEquals(len(usage_customers), 3)

    @vcr.use_cassette('get_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_single_customer(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1)
        c1_dict = {'country': 'United States', 'customer_id': '1',
                   'postal_code': '78232', 'name': '1018700'}
        self.assertDictEqual(usage_customer, c1_dict)

    @vcr.use_cassette('get_customer_not_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_single_customer_not_found(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1000000)
        self.assertIsNone(usage_customer)

    @vcr.use_cassette('create_new_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    # TODO: fix this once we find out why api gives a 404
    def no_test_create_new_customer(self):
        customer_info = {
            'name': 5551212,
            'country': 'US',
            'postal_code': 79762
        }
        new_customer = customers.create_customer(tests.CONNECTION, customer_info)
        self.assertDictContainsSubset(customer_info, new_customer)

    @vcr.use_cassette('delete_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_delete_customer(self):
        deleted_customer = customers.delete_customer(tests.CONNECTION, 1)
        self.assertEquals(deleted_customer, True)

    @vcr.use_cassette('get_customer_rules.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    # TODO: fix this once we find out why the api returns nothing
    def no_test_get_customer_rules(self):
        rules = customers.get_customer_rules(tests.CONNECTION, 2)
        self.assertEquals(rules, list)