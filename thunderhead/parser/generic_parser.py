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


class PayloadParser(object):
    """
    Payload parsing class.
    """
    ret = {}

    def __init__(self):
        pass

    def parse(self, payload):
        """
        Method to parse the response payloads from a vCloud Usage Meter response.

        :param payload:
        :return:
        """
        for info in payload.getchildren():
            tag = info.tag.split("}")[1][0:]
            text = info.text
            self.ret[tag] = text
        return self.ret