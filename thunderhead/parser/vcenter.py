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


def parse_all_vcenters(body):
    """
    Parse the response from a GET /api/vcenters
    This will return a list of dict where the dict
    is a representation of the vCenter.
    ret = [{
            'username': 'root',
            'instanceUuid': '137E2125-73EB-4E1B-BF03-2B6CD396E6AC',
            'monitor': 'false',
            'hostname': '172.16.214.129',
            'meter': 'true',
            'version': '5.5.0',
            'active': 'true',
            'fullname': 'VMware vCenter Server 5.5.0 build-1945287 (Sim)',
            'id': '1'
    }]
    :param body:
    :return list:
    """
    if body is None:
        return None
    # this is messy but it seems cleaner than dealing with the namespace
    vcenters = etree.fromstring(body)
    if len(vcenters) == 0:
        return None
    vcenter_list = []
    for vcenter in vcenters.getchildren():
        vcenter_dict = _parse_vcenter(vcenter)
        vcenter_list.append(vcenter_dict)
    return vcenter_list


def parse_vcenter(body):
    """
    Parse a single vCenter from GET /api/vcenter/{id}
    and from a POST /api/vcenter
    Returns a dict representation of a vCenter
    ret = {
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

    :param body:
    :return dict:
    """
    if body is None:
        return None
    vcenter = etree.fromstring(body)
    # lame. the extra <vcserver> tag seems pointless here..
    for vc in vcenter.getchildren():
        return _parse_vcenter(vc)


def _parse_vcenter(vcenter):
    v = {}
    for vcenter_info in vcenter.getchildren():
        # this is messy but it seems cleaner than dealing with the namespace
        tag = vcenter_info.tag.split("}")[1][0:]
        text = vcenter_info.text
        v[tag] = text
    return v