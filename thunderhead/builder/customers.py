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
    body = res.content
    pass


def create_customer(connection, customer):
    """
    Creates a customer

    :param customer:
    :return:
    """
    connection.command_path = "customer"
    req_type = 'POST'
    pass


def update_customer(connection, customer_id, customer):
    """
    Update a given customer with supplied customer info

    :param customer_id:
    :param customer:
    :return:
    """
    connection.command_path = "customer/{0}".format(customer_id)
    req_type = 'PUT'
    pass


def delete_customer(connection, customer_id):
    """
    Delete a specified customer, and delete rules associated with customer.

    :param customer_id:
    :return:
    """
    connection.command_path = 'customer/{0}'.format(customer_id)
    req_type = 'DELETE'
    pass