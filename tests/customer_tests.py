# -*- coding: utf-8 -*-
# Copyright 2014 Michael Rice <michael@michaelrice.org>
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

from __future__ import unicode_literals

import vcr

import tests
from thunderhead.builder import customers


class CustomerTests(tests.VCRBasedTests):
    # Test get all customers.
    @vcr.use_cassette('get_all_customers.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_all_customers(self):
        usage_customers = customers.get_all_customers(tests.CONNECTION)
        self.assertEquals(isinstance(usage_customers, list), True)
        self.assertEquals(len(usage_customers), 3)

    # Test get customer by ID
    @vcr.use_cassette('get_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_single_customer(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1)
        c1_dict = {'country': 'United States', 'customer_id': '1',
                   'postal_code': '78232', 'name': '1018700'}
        self.assertDictEqual(usage_customer, c1_dict)

    # Test customer not found
    @vcr.use_cassette('get_customer_not_found.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='none')
    def test_get_single_customer_not_found(self):
        usage_customer = customers.get_customer(tests.CONNECTION, 1000000)
        self.assertIsNone(usage_customer)

    # Test create new customer
    @vcr.use_cassette('create_new_customer.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_new_customer(self):
        customer_info = {
            'name': '15551212',
            'country': 'US',
            'postal_code': '79762'
        }
        new_customer = customers.create_customer(tests.CONNECTION, customer_info)
        # the api returns country name but expcets country code
        customer_info['country'] = 'United States'
        self.assertDictContainsSubset(customer_info, new_customer)

    # Test create new customer
    @vcr.use_cassette('create_new_customer_using_country_name.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_new_customer_using_country_name(self):
        customer_info = {
            'name': '15551212111',
            'country': 'United States',
            'postal_code': '79762'
        }
        with self.assertRaises(customers.InvalidCountryCodeException):
            customers.create_customer(tests.CONNECTION, customer_info)

    # Test create new customer
    @vcr.use_cassette('create_new_customer_no_country_code.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_new_customer_no_country_code(self):
        customer_info = {
            'name': '15551212',
            'postal_code': 'Unknown'
        }
        with self.assertRaises(customers.MissingProperty):
            customers.create_customer(tests.CONNECTION, customer_info)

    # Test Create new customer but duplicate found in system.
    @vcr.use_cassette('create_new_customer_duplicate_bad_request.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_create_new_customer_duplicate_found(self):
        customer_info = {
            'name': '5551212',
            'country': 'US',
            'postal_code': '79762'
        }
        with self.assertRaises(customers.DuplicateCustomerException):
            customers.create_customer(
                tests.CONNECTION,
                customer_info
            )

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

    @vcr.use_cassette('update_customer_name.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_update_customer_name(self):
        customer_info = {
            'name': '123333-updated',
            'country': 'US',
            'postal_code': '79762'
        }
        customer_id = 10
        updated_customer = customers.update_customer(tests.CONNECTION, customer_id, customer_info)
        self.assertIsInstance(updated_customer, dict)

    def test_customer_builder(self):
        customer = {
            'country': 'US',
            'name': '¿Cómo',
            'postal_code': '78555'
        }
        xml = customers._build_customer_payload(customer)
        res = b'<customer xmlns="http://www.vmware.com/UM"><name>&#191;C&#243;mo</name><country>US</country><postalCode>78555</postalCode></customer>'
        self.assertEqual(xml, res)
