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

import tests
from thunderhead.connection import Connection
from thunderhead.exceptions import MissingProperty


class ConnectionTests(tests.ThunderheadTests):

    def test_build_url_throws_missing_property(self):
        connection = Connection(port=8443, protocol="https")
        self.assertRaises(MissingProperty, connection.build_url)

    def test_build_url_strips_ending_slashes_from_command(self):
        host = "localhost"
        port = 8443
        command = "customers/"
        connection = Connection(host=host, port=port, command=command)
        path = connection.base_path
        proto = connection.protocol
        url = "{0}://{1}:{2}/{3}/customers".format(proto, host, port, path)
        self.assertEqual(url, connection.build_url())
