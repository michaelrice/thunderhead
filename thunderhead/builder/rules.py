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

from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

import requests

from thunderhead.parser import rules


class RuleNotFoundException(Exception):
    pass


class RuleDeletionException(Exception):
    pass


class RuleCreationException(Exception):
    pass


class RuleCreationDuplicateRule(Exception):
    pass


def get_all_rules(connection):
    """
    Get All Rules from vCloud Usage Meter

    :param connection:
    :return:
    """
    connection.command_path = "rules"
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code > 210:
        raise RuleNotFoundException(res.content)
    return rules.parse_all_rules(res.content)


def get_rule(connection, rule_id):
    """
    Get a specific rule based on its id.

    :param connection:
    :param rule_id:
    :return:
    """
    connection.command_path = "rule/{0}".format(rule_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code > 210:
        raise RuleNotFoundException(res.content)
    return rules.parse_rule(res.content)


def create_rule(connection, rule_info):
    """
    Create a new rule.

    rule_info = {
        'vcServer': '10.255.79.10',
        'customerName':'company23-A',
        'objectType':'VM',
        'valueType':'Unique ID',
        'value':'vm-10'
    }

    :param connection:
    :param rule_info:
    :return:
    """
    connection.command_path = 'rule'
    extra_headers = {
        connection.header_key: connection.token,
        'Content-Type': 'text/xml'
    }
    url = connection.build_url()
    rule_data = _build_rule_payload(rule_info)
    verify_ssl = connection.verify_ssl
    res = requests.post(url, headers=extra_headers,
                        data=rule_data,
                        verify=verify_ssl)
    if res.status_code == 201:
        return rules.parse_rule(res.content)

    if res.status_code == 403 and "Rule already exists" in res.text:
        raise RuleCreationDuplicateRule("Rule already exists")

    raise RuleCreationException("Error creating rule: {0} => {0}".format(
        res.status_code, res.content
    ))


def update_rule(connection, rule_info):
    pass


def delete_rule(connection, rule_id):
    """
    Delete a given rule from vCloud Usage Meter based on its id

    :param connection:
    :param rule_id:
    :return:
    """
    connection.command_path = 'rule/{0}'.format(rule_id)
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    extra_headers = {connection.header_key: connection.token}
    res = requests.delete(url, headers=extra_headers, verify=verify_ssl)
    if res.status_code != 204:
        raise RuleDeletionException("Error: {0} => {1}".format(
            res.status_code, res.content))
    return True


def _build_rule_payload(rule_info):
    """
    rule_info = {
        'vcServer': '10.255.79.10',
        'customerName':'company23-A',
        'objectType':'VM',
        'valueType':'Unique ID',
        'value':'vm-10'
    }

    <rule xmlns="http://www.vmware.com/UM">
        <vcServerId>10.255.79.10</vcServerId>
        <customerName>company23-A</customerName>
        <objectType>VM</objectType>
        <valueType>Unique ID</valueType>
        <value>vm-10</value>
    </rule>

    From schema from VMware:
    <xs:complexType name="NewRule">
      <xs:sequence>
        <xs:element name="vcServerHost" type="xs:string" minOccurs="0"/>
        <xs:element name="customerName" type="xs:string"/>
        <xs:element name="objectType" type="objectType"/>
        <xs:element name="valueType" type="valueType"/>
        <xs:element name="value" type="xs:string" minOccurs="0"/>
      </xs:sequence>
    </xs:complexType>

    :param rule_info:
    :return:
    """
    attribs = {
        'xmlns': 'http://www.vmware.com/UM'
    }
    root = Element('rule', attribs)
    vcenter = SubElement(root, 'vcServerHost')
    vcenter.text = str(rule_info['vcServerHost'])
    customer = SubElement(root, 'customerName')
    customer.text = str(rule_info['customerName'])
    object_type = SubElement(root, 'objectType')
    object_type.text = str(rule_info['objectType'])
    value_type = SubElement(root, 'valueType')
    value_type.text = str(rule_info['valueType'])
    value = SubElement(root, 'value')
    value.text = str(rule_info['value'])
    return tostring(root)
