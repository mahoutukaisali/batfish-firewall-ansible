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
from ansible.module_utils.six.moves.urllib.parse import urlsplit
from ansible.module_utils.network.common.config import NetworkConfig
from ansible.errors import AnsibleError

from difflib import Differ

try:
  # pylint: disable=W0611
  # W0611:Unused display imported from __main__
  from __main__ import display
except ImportError:
  # pylint: disable=C0412
  # C0412:Imports from package ansible are not grouped
  from ansible.utils.display import Display
  display = Display()

class ActionModule(_ActionModule):
  supported_params = [
    'before',
    'after',
    'ignore_str',
    'ignore_regexp'
  ]

  def file_search(self, before, after):
    before_file = Path(before)
    after_file = Path(after)
    if before_file.is_file():
      pass
    else:
      return 'before file does not exist.'

    if after_file.is_file():
      pass
    else:
      return 'after file does not exist.'

  def before_after_diff_list(self, before, after, ignore_regex=''):
    d = Differ()
    str1_list = []
    str2_list = []

    with open(before, 'r') as f:
      str1 = f.readlines()
      for i in str1:
        #if i.find(ignore_str) != -1:
        #  replaced_str1 = i.replace(ignore_str, '')
        #  str1_list.append(replaced_str1)
        if re.findall(ignore_regex, i):
          replace_regex = re.sub(ignore_regex, '', i)
          str1_list.append(replace_regex)
        else:
          str1_list.append(i)

    with open(after, 'r') as f:
      str2 = f.readlines()
      for i in str2:
        #if i.find(ignore_str) != -1:
        #  replaced_str2 = i.replace(ignore_str, '')
        #  str2_list.append(replaced_str2)
        if re.findall(ignore_regex, i):
          replace_regex = re.sub(ignore_regex, '', i)
          str2_list.append(replace_regex)
        else:
          str2_list.append(i)
    #result_list = list(d.compare(str1, str2))
    result_list = list(d.compare(str1_list, str2_list))
    return result_list


  def plus_result_list(self, result):
    around_list = []
    around_list2 = []
    for i in result:
      if i.startswith('+'):
        #+から始まる行の番号を取得
        index_start_num = result.index(i)
        #+から始まる行の二つ上の番号を取得
        before_around_num = index_start_num - 5
        #+から始まる行の二つ下の番号を取得
        after_around_num = index_start_num + 5
        around_num_list = result[before_around_num:after_around_num]
        around_list.append('#######################')
        around_list.extend(around_num_list)
        for a in around_list:
          if not a.startswith('?'):
            around_list2.append(a)
          else:
            continue

        #for r in range(around_num):
        #  plus_list.add(result[r])
        #  print(plus_list)
      else:
        continue

    return around_list2


  def before_after_diff_message(self, result):
    result_msg = '\n'.join(result)
    return result_msg


  def run(self, tmp=None, task_vars=None):
    del tmp

    # モジュールを実行する
    # ただし、このモジュールは何もしない
    result = super(ActionModule, self).run(task_vars=task_vars)

    #
    # モジュール実行後の後工程処理
    #

    before = self._task.args.get('before')
    after = self._task.args.get('after')
    ignore_regexp = self._task.args.get('ignore_regexp')


    search_result = self.file_search(before, after)
    result_list = self.before_after_diff_list(before, after, ignore_regexp)
    parsed_list = self.plus_result_list(result_list)

    try:
      result_list = self.before_after_diff_list(before, after, ignore_regexp)
      msg = self.before_after_diff_message(parsed_list)
      result['msg'] = msg
      return result
    except FileNotFoundError:
      msg = search_result
      result['failed'] = True
      result['msg'] = msg
      return result


