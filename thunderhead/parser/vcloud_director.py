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
from thunderhead.parser.generic_parser import PayloadParser


def parse_all_vcd(body):
    """
    Parse the response from a GET /api/getAllVcd
    This will return a list of dict where the dict
    is a representation of the vcd.

    :param body:
    :return:
    """
    if body is None:
        return None
    pass


def parse_vcd(body):
    vcd = etree.fromstring(body)
    return _parse_vcd(vcd)


def _parse_vcd(vcloud):
    vcd_parser = PayloadParser()
    return vcd_parser.parse(vcloud)