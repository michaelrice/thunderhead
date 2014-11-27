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
from thunderhead.exceptions import VCloudDirectorException

from thunderhead.parser import vcloud_director


def get_all_vcd(connection):
    """
    Get a list of all vCloud Director Servers.

    :param connection:
    :return:
    """
    raise NotImplementedError
    connection.command_path = "getAllVcd"
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    try:
        res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    except Exception:
        raise VCloudDirectorException("Connection error occurred")
    if res.status_code > 210:
        raise VCloudDirectorException("Unable to fetch all VCD: {0} => {1}".
                                      format(res.status_code, res.content))
    body = res.content
    return vcloud_director.parse_all_vcd(body)


def _build_vcd(vcd_object):
    """
    <Vcd xmlns="http://www.vmware.com/UM">
        <hostname>10.255.79.123</hostname>
        <username>admin</username>
        <password>vmware123</password>
    </Vcd>

    :param vcd_object:
    :return:
    """
    attribs = {
        'xmlns': 'http://www.vmware.com/UM'
    }
    root = Element('vcServer', attribs)
    host = SubElement(root, 'hostname')
    host.text = str(vcd_object['hostname'])
    username = SubElement(root, 'username')
    username.text = str(vcd_object['username'])
    password = SubElement(root, 'password')
    password.text = str(vcd_object['password'])
    return tostring(root)


def create_vcd_server(connection, vcd_object):
    """
    vcd should be a dict that looks like:

    {
        'hostname': '10.2.3.4',
        'username': 'root',
        'password': 'my password'
    }

    :raises VCloudDirectorException:
    :param connection:
    :return dict:
    """
    connection.command_path = "vcd"
    extra_headers = {
        connection.header_key: connection.token,
        'Content-Type': 'text/xml'
    }
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    vcd_data = _build_vcd(vcd_object)
    res = requests.post(url, headers=extra_headers,
                        data=vcd_data,
                        verify=verify_ssl)
    if res.status_code > 210:
        raise VCloudDirectorException("Unable to create a vcd: {0} => {1}".format(
            res.status_code, res.content
        ))
    return vcloud_director.parse_vcd(res.content)
