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

import re
from xml.etree import ElementTree as etree


def parse_all_vcenters(body):
    if body is None:
        return None
    # this is messy but it seems cleaner than dealing with the namespace
    body = re.sub(' xmlns="[^"]+"', '', body, count=1)
    vcenters = etree.fromstring(body)
    if len(vcenters) == 0:
        return None
    vcenter_list = []
    for vcenter in vcenters.getchildren():
        vcenter_dict = _parse_vcenter(vcenter)
        vcenter_list.append(vcenter_dict)
    return vcenter_list


def parse_vcenter(body):
    if body is None:
        return None
    # this is messy but it seems cleaner than dealing with the namespace
    body = re.sub(' xmlns="[^"]+"', '', body, count=1)
    vcenter = etree.fromstring(body)
    # lame. the extra <vcserver> tag seems pointless here..
    for vc in vcenter.getchildren():
        return _parse_vcenter(vc)


def _parse_vcenter(vcenter):
    v = {}
    for vcenter_info in vcenter.getchildren():
        tag = vcenter_info.tag
        text = vcenter_info.text
        v[tag] = text
    return v