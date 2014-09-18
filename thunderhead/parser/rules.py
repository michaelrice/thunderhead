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


def parse_all_rules(body):
    if body is None:
        return None
    rules = etree.fromstring(body)
    if len(rules) == 0:
        return None
    rule_list = []
    for rule in rules.getchildren():
        rule_dict = _parse_rule(rule)
        rule_list.append(rule_dict)
    return rule_list


def parse_rule(body):
    if body is None:
        return None
    rule = etree.fromstring(body)
    return _parse_rule(rule)


def _parse_rule(rule):
    v = {}
    for rule_info in rule.getchildren():
        # this is messy but it seems cleaner than dealing with the namespace
        tag = rule_info.tag.split("}")[1][0:]
        text = rule_info.text
        v[tag] = text
    return v