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

import vcr

import tests

from thunderhead.builder import reports


class ReportTests(tests.VCRBasedTests):

    @vcr.use_cassette('get_report_list.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_report_list(self):
        report_list = reports.get_report_list(tests.CONNECTION)
        self.assertIsInstance(report_list, list)

    @vcr.use_cassette('get_report_by_id.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_report_by_id(self):
        report = reports.get_report(tests.CONNECTION, 1, date_from=2014091200,
                                    date_to=2014091800)
        self.assertIsNotNone(report)

    @vcr.use_cassette('get_report_by_id_bad_request.yaml',
                      cassette_library_dir=tests.fixtures_path,
                      record_mode='once')
    def test_get_report_by_id_bad_request(self):
        with self.assertRaises(reports.ReportException):
            reports.get_report(tests.CONNECTION, 1, date_from=2014091200,
                               date_to=20140918)
