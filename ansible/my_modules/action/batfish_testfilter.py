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
import csv

import textfsm
from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.question import *
from pybatfish.datamodel import *


class ActionModule(_ActionModule):

  def run(self, tmp=None, task_vars=None):
    del tmp

    # モジュールを実行する
    # ただし、このモジュールは何もしない
    result = super(ActionModule, self).run(task_vars=task_vars)

    import csv
    #
    # モジュール実行後の後工程処理
    #

    snapshot_name = self._task.args.get('snapshot_name')
    snapshot_path = self._task.args.get('snapshot_path')
    network_name = self._task.args.get('network_name')

    csv_file_path = self._task.args.get('csv_file_path')

    csv_file_list = []
    PASS = "PASS"
    FAIL = "FAIL"

    result = {}
    result_list = []
    with open(csv_file_path) as f:

      csv_file_list = [x for x in csv.DictReader(f)]

    answer_list = []
    load_questions()
    bf_set_network(network_name)
    bf_init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
    result = {}
    for csv in csv_file_list:
      intend_condition = csv.get('intend_condition')
      test_id = csv.get('test_id')
      src = csv.get('src')
      dest = csv.get('dest')
      acl = csv.get('acl_name')
      node = csv.get('node')
      application = csv.get('application')

      if intend_condition == '' or intend_condition == None:
        result['failed'] = True
        result['msg'] = 'intend_condition parameter is required.'
        return result

      if test_id == '' or test_id == None:
        result['failed'] = True
        result['msg'] = 'test_id parameter is required.'
        return result

      #srcは必ず必要なパラメータ
      if src == '':
        result['failed'] = True
        result['msg'] = 'src parameter is required.'
        return result

      if node == '':
        result['failed'] = True
        result['msg'] = 'node parameter is required.'
        return result

      if acl == '':
        result['failed'] = True
        result['msg'] = 'acl parameter is required.'
        return result

      if dest != '' and application != '':

        ip_flow = HeaderConstraints(srcIps=src,
                                    dstIps=dest,
                                    applications=application)
        answer = bfq.testFilters(headers=ip_flow,
                                 nodes=node,
                                 filters=acl).answer()
        show = answer.frame()
        answer = show.to_json()
        json_answer = json.loads(answer)
        json_answer["Test_id"] = test_id
        json_answer["Intend_condition"] = intend_condition
        answer_list.append(json_answer)

      elif dest != '' and application == '':
        ip_flow = HeaderConstraints(srcIps=src,
                                    dstIps=dest)
        answer = bfq.testFilters(headers=ip_flow,
                                 nodes=node,
                                 filters=acl).answer()
        show = answer.frame()
        answer = show.to_json()
        json_answer = json.loads(answer)
        json_answer["Test_id"] = test_id
        json_answer["Intend_condition"] = intend_condition
        answer_list.append(json_answer)

      elif application != '' and dest == '':
        ip_flow = HeaderConstraints(srcIps=src,
                                    applications=application)
        answer = bfq.testFilters(headers=ip_flow,
                                 nodes=node,
                                 filters=acl).answer()
        show = answer.frame()
        answer = show.to_json()
        json_answer = json.loads(answer)
        json_answer["Test_id"] = test_id
        json_answer["Intend_condition"] = intend_condition
        answer_list.append(json_answer)

    result['batfish_result'] = answer_list


    for answer in answer_list:
      action = answer['Action']
      action_num = action["0"]
      condition = answer["Intend_condition"]
      test_id = answer["Test_id"]

      if action_num != condition.upper():
        result['failed'] = True
        result_list.append('{0}. test_id {1} test is failed.'.format(FAIL, test_id))
      else:
        result_list.append(PASS)
        result_list.append('{0}. {1} test is passed.'.format(PASS, test_id))

    result['msg'] = result_list
    return result
