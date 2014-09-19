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


def parse_reports(body):
    if body is None:
        return
    report_types_list = etree.fromstring(body)
    report_list = []
    for report in report_types_list.getchildren():
        report_list.append(_parse_report(report))
    return report_list


def _parse_report(report):
    for element in report:
        if element.tag == 'link':
            report_id = element.attrib['href'].split('/')[-1]
            report_name = element.attrib['rel']

            return {
                'report_id': report_id,
                'report_name': report_name
            }