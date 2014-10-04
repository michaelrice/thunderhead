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

from thunderhead.parser import vcenter


def get_all_vcenters(connection):
    """
    Get a list of all vCenters
    List will contain a dict representation of a vCenter
    for each vCenter. The dict will look like:
    {
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

    :raises VCenterException:
    :param connection:
    :return list:
    """
    connection.command_path = "vcenters"
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    try:
        res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    except Exception:
        raise VCenterException("Connection error occurred.")
    if res.status_code > 210:
        raise VCenterException("Unable to fetch all vCenters: {0} => {1}".
                               format(res.status_code, res.content))
    body = res.content
    return vcenter.parse_all_vcenters(body)


def create_vcenter(connection, vcenter_obj):
    """
    vcenter should be a dict that looks like:

    {
        'hostname': '10.2.3.4',
        'username': 'root',
        'password': 'my password',
        'monitor': 'true'
    }

    :raises VCenterException:
    :param connection:
    :return dict:
    """
    connection.command_path = "vcenter"
    extra_headers = {
        connection.header_key: connection.token,
        'Content-Type': 'text/xml'
    }
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    vcenter_data = _build_vcenter(vcenter_obj)
    res = requests.post(url, headers=extra_headers,
                        data=vcenter_data,
                        verify=verify_ssl)
    if res.status_code > 210:
        raise VCenterException("Unable to create a vCenter: {0} => {1}".format(
            res.status_code, res.content
        ))
    return vcenter.parse_vcenter(res.content)


def get_vcenter(connection, vcenter_id):
    """
    Get a single vCenter based on its id.
    This will produce a dict representation
    of a vCenter:
    {
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

    :raises VCenterException:
    :param connection:
    :param vcenter_id:
    :return:
    """
    connection.command_path = "vcenter/{0}".format(vcenter_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code > 210:
        raise VCenterException("Unable to retrieve vCenter: {0} => {1}".format(
            res.status_code, res.content
        ))
    body = res.content
    return vcenter.parse_vcenter(body)


def update_vcenter(connection, vcenter_info):
    connection.command_path = "customers"
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl


def delete_vcenter(connection, vcenter_id):
    connection.command_path = "customers/{0}".format(vcenter_id)
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl


def _build_vcenter(vcenter_info):
    """
    <VC xmlns="http://www.vmware.com/UM">
        <hostname>10.255.79.5</hostname>
        <username>root</username>
        <password>vmware</password>
        <monitor>true</monitor>
    </VC>

    :param vcenter_info:
    :return:
    """
    attribs = {
        'xmlns': 'http://www.vmware.com/UM'
    }
    root = Element('vcServer', attribs)
    host = SubElement(root, 'hostname')
    host.text = str(vcenter_info['hostname'])
    username = SubElement(root, 'username')
    username.text = str(vcenter_info['username'])
    password = SubElement(root, 'password')
    password.text = str(vcenter_info['password'])
    monitor = SubElement(root, 'monitor')
    monitor.text = str(vcenter_info['monitor'])
    return tostring(root)


class VCenterException(Exception):
    pass
