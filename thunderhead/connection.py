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

from .exceptions import MissingProperty


class Connection:
    def __init__(self, **kwargs):
        self.token = kwargs.get("token")
        self.port = 8443
        if kwargs.get("port"):
            self.port = kwargs.get("port")
        self.host = kwargs.get("host")
        self.header_key = "x-usagemeter-authorization"
        self.base_path = "um/api"
        self.protocol = "https"
        if kwargs.get("protocol"):
            self.protocol = kwargs.get("protocol")
        self.command_path = kwargs.get("command")
        self.verify_ssl = kwargs.get('verify_ssl')

    def build_url(self):
        """
        Builds a valid URL for use in connecting to vCloud Usage Meter

        :rtype : str
        """
        self._check_required_url_properties()
        self._strip_command_slashes()
        return "{0}://{1}:{2}/{3}/{4}".format(
            self.protocol,
            self.host,
            self.port,
            self.base_path,
            self.command_path
        )

    def _strip_command_slashes(self):
        """
        Removes any trailing slashes from the command path
        """
        if self.command_path.endswith("/"):
            self.command_path = self.command_path[:-1]

    def _check_required_url_properties(self):
        """
        Verifies that all required properties are set before calling
        the build_url method
        """
        if not self.host:
            raise MissingProperty('host')
        if not self.command_path:
            raise MissingProperty('command_path')
