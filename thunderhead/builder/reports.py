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

from thunderhead.parser import reports


def get_report_list(connection):
    connection.command_path = 'reports'
    extra_headers = {connection.header_key: connection.token}
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url=url, headers=extra_headers, verify=verify_ssl)
    if res.status_code == 200:
        return reports.parse_reports(res.content)
    raise ReportException("Error getting reports: {0} => {1}".format(
        res.status_code, res.content
    ))


def get_report(connection, report_id, date_from, date_to):
    connection.command_path = 'report/{0}'.format(report_id)
    extra_headers = {connection.header_key: connection.token}
    query_params = {
        'dateFrom': date_from,
        'dateTo': date_to
    }
    url = connection.build_url()
    verify_ssl = connection.verify_ssl
    res = requests.get(url, headers=extra_headers, params=query_params, verify=verify_ssl)
    if res.status_code == 200:
        return res.content
    raise ReportException("Error fetching report: {0} => {1}".format(
        res.status_code, res.content
    ))


class ReportException(Exception):
    pass