# coding=utf-8
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

from __future__ import unicode_literals

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

import requests

from thunderhead.parser import customers


def get_all_customers(connection):
    """
    Return representation of all customers

    :return:
    """
    connection.command_path = "customers"
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code > 210:
        return
    body = res.content
    return customers.parse_all_customers(body)


def get_customer(connection, customer_id):
    """
    Returns a single customer given a customer id

    :param customer_id:
    :return:
    """
    connection.command_path = "customer/{0}".format(customer_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    body = res.content
    if res.status_code > 210:
        return
    return customers.parse_customer(body)


def get_customer_rules(connection, customer_id):
    """
    Returns a list of customer rules given a customer id

    :param customer_id:
    :return:
    """
    connection.command_path = "customer/{0}/rules".format(customer_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code > 210:
        raise CustomerNotFoundException(res.content)
    body = res.content
    return customers.parse_customer_rules(body)


def _build_customer_payload(customer):
    """
    <customer xmlns="http://www.vmware.com/UM">
        <name>Customer Name</name>
        <country>US</country>
        <postalCode>90210</postalCode>
    </customer>
    """
    if not 'country' in customer:
        raise MissingProperty("Missing required 'country'.")
    if not 'name' in customer:
        raise MissingProperty("Missing required 'name'")
    if not 'postal_code' in customer:
        raise MissingProperty("Missing required 'postal_code'")

    attribs = {
        'xmlns': 'http://www.vmware.com/UM'
    }
    root = Element('customer', attribs)
    name = SubElement(root, 'name')
    name.text = customer['name']
    country = SubElement(root, 'country')
    country.text = customer['country']
    postal = SubElement(root, 'postalCode')
    postal.text = customer['postal_code']
    return tostring(root)


def create_customer(connection, customer):
    """
    Creates a customer

    The customer param should be a dict like:
    {
        'name': 123456,
        'country': 'US',
        'postal_code': 78232
    }

    :param connection:
    :param customer:
    :return:
    """
    connection.command_path = "customer"
    extra_headers = {
        connection.header_key: connection.token,
        'Content-Type': 'text/xml'
    }
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    customer_data = _build_customer_payload(customer)
    res = requests.post(url, headers=extra_headers,
                        data=customer_data,
                        verify=verify_ssl)
    if res.status_code == 400 and res.content == b'The Customer name must be unique.':
        raise DuplicateCustomerException(res.content)
    elif res.status_code == 400 and b'not a valid country code' in res.content:
        raise InvalidCountryCodeException(res.content)
    elif res.status_code == 201:
        return customers.parse_customer(res.content)
    else:
        raise UnExpectedCustomerException(res.content)


def update_customer(connection, customer_id, customer):
    """
    Update a given customer with supplied customer info

    :param customer_id:
    :param customer:
    :return:
    """
    connection.command_path = "customer/{0}".format(customer_id)
    extra_headers = {
        connection.header_key: connection.token,
        'Content-Type': 'text/xml'
    }
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    customer_data = _build_customer_payload(customer)
    res = requests.put(url, headers=extra_headers,
                       data=customer_data,
                       verify=verify_ssl)
    if res.status_code == 400 and res.content == b'The Customer name must be unique.':
        raise DuplicateCustomerException(res.content)
    elif res.status_code == 400 and b'not a valid country code' in res.content:
        raise InvalidCountryCodeException(res.content)
    elif res.status_code == 200:
        return customers.parse_customer(res.content)
    else:
        raise UnExpectedCustomerException(res.content)


def delete_customer(connection, customer_id):
    """
    Delete a specified customer, and delete rules associated with customer.

    :param customer_id:
    :return:
    """
    connection.command_path = 'customer/{0}'.format(customer_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.delete(url, headers=extra_headers, verify=verify_ssl)
    if res.status_code == 204:
        return True
    raise CustomerDeletionException(res.content)


class DuplicateCustomerException(Exception):
    pass


class CustomerNotFoundException(Exception):
    pass


class UnExpectedCustomerException(Exception):
    pass


class CustomerDeletionException(Exception):
    pass


class MissingProperty(Exception):
    pass


class InvalidCountryCodeException(Exception):
    pass

