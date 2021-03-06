'''
This is the ansible module using batfish
'''
# -*- coding: utf-8 -*-

# pylint: disable=bad-option-value
# pylint: disable=C0611

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

from ansible.plugins.action.normal import ActionModule as _ActionModule
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleError

import json
import csv

from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.datamodel import *


class ActionModule(_ActionModule):

    def run(self, tmp=None, task_vars=None):
        del tmp

        # モジュールを実行する
        # ただし、このモジュールは何もしない
        result = super(ActionModule, self).run(task_vars=task_vars)

        #
        # モジュール実行後の後工程処理
        #

        snapshot_name = self._task.args.get('snapshot_name')
        snapshot_path = self._task.args.get('snapshot_path')
        network_name = self._task.args.get('network_name')

        csv_file_path = self._task.args.get('csv_file_path')

        PASS = "PASS"
        FAIL = "FAIL"

        result = {}
        result_list = []

        with open(csv_file_path, mode='r') as f:
            csv_file_list = [x for x in csv.DictReader(f)]

        answer_list = []

        # Batfishの質問、スナップショット及びノードを読見込む
        load_questions()

        if network_name and snapshot_name:
            bf_set_network(network_name)
            bf_init_snapshot(snapshot_path, name=snapshot_name, overwrite=True)
        else:
            bf_set_network()
            bf_init_snapshot(snapshot_path, overwrite=True)

        for c in csv_file_list:
            expect_condition = c.get('expect_condition')
            test_id = c.get('test_id')
            src = c.get('src')
            dest = c.get('dest')
            acl = c.get('acl_name')
            node = c.get('node')
            application = c.get('application')
            src_int = c.get('src_int')
            dest_int = c.get('dest_int')


            if expect_condition == '' or expect_condition == None:
                result['failed'] = True
                result['msg'] = 'expect_condition parameter is required.'
                return result

            if expect_condition != 'deny' and expect_condition != 'permit':
                result['failed'] = True
                result['msg'] = 'expect_condition parameter should be permit or deny. '
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

            if src_int != '' and node == '':
                result['failed'] = True
                result['msg'] = 'node must be specified if you want to test src_int.'
                return result

            if acl == '' or acl == None:
                ip_flow = HeaderConstraints(srcIps=src)

                answer = bfq.testFilters(headers=ip_flow,
                                         nodes=node).answer()
                show = answer.frame()
                answer = show.to_json()
                json_answer = json.loads(answer)
                json_answer["Test_id"] = test_id
                json_answer["expect_condition"] = expect_condition
                answer_list.append(json_answer)

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
                json_answer["expect_condition"] = expect_condition
                answer_list.append(json_answer)

            # 一つ上の条件が一致した場合は以下セクションを読み込む必要がないのでelifを使う
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
                json_answer["expect_condition"] = expect_condition
                answer_list.append(json_answer)

            elif dest == '' and application != '':
                ip_flow = HeaderConstraints(srcIps=src,
                                            applications=application)
                answer = bfq.testFilters(headers=ip_flow,
                                         nodes=node,
                                         filters=acl).answer()
                show = answer.frame()
                answer = show.to_json()
                json_answer = json.loads(answer)
                json_answer["Test_id"] = test_id
                json_answer["expect_condition"] = expect_condition
                answer_list.append(json_answer)

            # あるノードのintに着信したパケットが出力intとして指定したintで
            # どのように処理されるかテストする
            # nodeの指定がない場合はエラーになるよう上で実装済
            #
            # ある着信がdeny or permitをテストしたい時のセクション

            #ノードとintを正確に指定しても動作しないので保留

            #if src_int != '' and dest_int == '' and application == '' and dest == '':
            #    flow = HeaderConstraints(srcIps=src)
            #    answer = bfq.testFilters(headers=flow,
            #             startLocation="@enter(" + node + "[" + src_int + "])",
            #             filters="@out(" + dest_int + ")").answer()
#
            #    show = answer.frame()
            #    answer = show.to_json()
            #    json_answer = json.loads(answer)
            #    json_answer["Test_id"] = test_id
            #    json_answer["expect_condition"] = expect_condition
            #    answer_list.append(json_answer)

            #if src_int != '' and dest_int != '' and application != '' and dest != '' and application != '':
            #    flow = HeaderConstraints(srcIps=src,
            #                  dstIps=dest,
            #                  applications=application)
            #    answer = bfq.testFilters(headers=flow,
            #             startLocation="@enter(" + node + "[" + src_int + "])",
            #             filters="@out(" + dest_int + ")").answer()
#
            #    show = answer.frame()
            #    answer = show.to_json()
            #    json_answer = json.loads(answer)
            #    json_answer["Test_id"] = test_id
            #    json_answer["expect_condition"] = expect_condition
            #   answer_list.append(json_answer)


        result['batfish_result'] = answer_list


        for answer in answer_list:
            action = answer['Action']
            action_num = action["0"]
            condition = answer["expect_condition"]
            test_id = answer["Test_id"]

            # Batfishが出す結果(DENY or PERMIT)とexpect_conditionがマッチしなければFAIL
            if action_num != condition.upper():
                result['failed'] = True
                result_list.append('test_id {0} is {1}.'.format(test_id, FAIL))
            else:
                result_list.append('test_id {0} is {1}.'.format(test_id, PASS))

        result['msg'] = result_list
        return result
