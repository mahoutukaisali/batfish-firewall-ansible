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

import os
import json
import sys
import re
#textfsmのパスをnotebookに渡す
sys.path.append('/Users/lisago/python/ansible/venv/lib/python3.7/site-packages')
import textfsm
from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.question import *
from pybatfish.datamodel import *


class ActionModule(_ActionModule):
  supported_params = [
    'src',
    'dest',
    'protocol',
    'condition',
    'node',
    'acl_name'
  ]


