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

from xml.etree import ElementTree as etree


def parse_all_customers(body):
    if body is None:
        return None
    customers = etree.fromstring(body)
    if len(customers) == 0:
        return None
    customer_list = []
    for customer in customers.getchildren():
        customer_dict = _parse_customer(customer)
        customer_list.append(customer_dict)
    return customer_list


def parse_customer(body):
    if body is None:
        return None
    customer = etree.fromstring(body)
    return _parse_customer(customer)


# TODO: fix this once we know why api returns nothing
def parse_customer_rules(body):
    pass


def _parse_customer(customer):
    c = {}
    for customer_info in customer:
        tag = customer_info.tag
        text = customer_info.text
        if tag == 'id':
            c['customer_id'] = text
        if tag == 'postalCode':
            c['postal_code'] = text
        if tag == 'name':
            c['name'] = text
        if tag == 'country':
            c['country'] = text
    return c