# -*- coding: utf-8 -*-
# pylint: disable=E0611,C0111
# E0611:No name 'urllib' in module '_MovedItems'
# C0111:Missing class docstring
# flake8: disable=E111,E114

# (c) 2018, Lisa Go (@lisago)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# python2でもpython3の機能を使えるようにする
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from pathlib import Path
import re

from ansible.plugins.action.normal import ActionModule as _ActionModule
from ansible.module_utils._text import to_text
#from ansible.module_utils.six.moves.urllib.parse import urlsplit
from ansible.module_utils.network.common.config import NetworkConfig
from ansible.errors import AnsibleError

import os
import json
import sys
import re

from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.question import *
from pybatfish.datamodel import *


class ActionModule(_ActionModule):
  supported_params = [
    'snapshot_name',
    'snapshot_path',
    'network_name',
    'src',
    'dest',
    'protocol',
    'condition',
    'node',
    'acl_name'
  ]

  def create_src_list(self, src):
    src_list = []
    if isinstance(src, list):
      src_list.extend(src)
      return src_list
    elif isinstance(src, str):
      src_list.append(src)
      return src_list

  def create_dest_list(self, dest=None):
    dest_list = []
    if isinstance(dest, list):
      dest_list.extend(dest)
      return dest_list
    elif isinstance(dest, str):
      dest_list.append(dest)
      return dest_list

  def create_application_list(self, application=None):
    application_list = []
    if isinstance(application, list):
      application_list.extend(application)
      return application_list
    elif isinstance(application, str):
      application_list.append(application)
      return application_list

  def create_acl_list(self, acl_name):
    acl_name_list = []
    if isinstance(acl_name, list):
      acl_name_list.extend(acl_name)
      return acl_name_list
    elif isinstance(acl_name, str):
      acl_name_list.append(acl_name)
      return acl_name_list

  def create_node_list(self, node):
    node_list = []
    if isinstance(node, list):
      node_list.extend(node)
      return node_list
    elif isinstance(node, str):
      node_list.append(node)
      return node_list

  def create_condition_list(self, condition):
    condition_list = []
    condition_list.append(condition)
    return condition_list

  def answer_testfilters_question(self, src_list, node_list, acl_list, dest_list=None, application_list=None):
    for acl in acl_list:
      acl = acl

    for node in node_list:
      node = node

    if dest_list is not None:
      for dest in dest_list:
        dest = dest

    if application_list is not None:
      for application in application_list:
        application = application

    for src in src_list:
      src = src

      ip_flow = HeaderConstraints(srcIps=src,
                                  dstIps=dest)
      answer = bfq.testFilters(headers=ip_flow,
                               nodes=node,
                               filters=acl).answer()

      show = answer.frame()
    return show.to_json()

  #def answer_testfilters_question(self, src_list, node_list, acl_list, dest_list=None, application_list=None):
#
  #  ip_flow = HeaderConstraints(srcIps=src_list,
  #                              dstIps=dest_list)
  #  answer = bfq.testFilters(headers=ip_flow,
  #                           nodes=node_list,
  #                           filters=acl_list).answer()
  #
  #  show = answer.frame()
  #  return show.to_json()

  def judge_condition(self, condition, answer):

    PASS = 'PASS'
    FAIL = 'FAIL'

    j = json.loads(answer)
    flow = j['Action']
    flow2 = flow["0"]
    if flow2.upper() == condition.upper():
      return PASS
    else:
      return FAIL


  def run(self, tmp=None, task_vars=None):
    del tmp

    # モジュールを実行する
    # ただし、このモジュールは何もしない
    result = super(ActionModule, self).run(task_vars=task_vars)

    #
    # モジュール実行後の後工程処理
    #

    src = self._task.args.get('src')
    dest = self._task.args.get('dest')
    snapshot_name = self._task.args.get('snapshot_name')
    snapshot_path = self._task.args.get('snapshot_path')
    network_name = self._task.args.get('network_name')
    application = self._task.args.get('application')
    condition = self._task.args.get('condition')
    node = self._task.args.get('node')
    acl_name = self._task.args.get('acl_name')

    src_list = self.create_src_list(src)
    dest_list = self.create_dest_list(dest)
    application_list = self.create_application_list(application)
    condition_list = self.create_condition_list(condition)
    node_list = self.create_node_list(node)
    acl_list = self.create_acl_list(acl_name)


    load_questions()
    bf_set_network(network_name)
    bf_init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
    #init_snapshot(self, snapshot_name, snapshot_path)
    msg = self.answer_testfilters_question(src_list, node_list, acl_list, dest_list, application_list)
    #msg = self.answer_testfilters_question(src, node, acl_name, dest, application)
    answer = msg
    msg1 = self.judge_condition(condition, answer)

    result['batfish_result'] = json.loads(msg)
    #result['judge'] = json.loads(msg1)

    if msg1 == 'PASS':
      result['msg'] = 'PASS'
      return result
    else:
      result['failed'] = True
      return result


