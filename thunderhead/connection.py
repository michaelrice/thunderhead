#
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
#


class Connection:
    def __init__(self, **kwargs):
        self.token = kwargs.get("token")
        self.port = 8443
        if kwargs.get("port"):
            self.port = kwargs.get("port")
        self.host = kwargs.get("host")
        self.header_key = "x-usagemeter-authorization"
        self.path = "/um/api/"
        self.protocol = "https"
        if kwargs.get("protocol"):
            self.protocol = kwargs.get("protocol")

    def build_url(self):
        return "{0}://{1}:{2}/{3}".format(self.protocol, self.host, self.port,
                                          self.path)
