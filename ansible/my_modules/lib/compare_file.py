#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,E0611,E0401

# LISA GO (@LisaGo)

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}

DOCUMENTATION = """
---
module: file_compare
version_added: "2.8"
author: "LISA GO (@LisaGo)"
short_description: Compare files there exist differences or not.
description:
  - Compare files and to see differences.
  - This module created by assuming that to compare between log file created before execute and log file created after execute.
options:
  before:
    description:
      - The file that you would compare with 'after'.
  after:
    description:
      - The file that you would compare with 'before'.
"""

EXAMPLES = r"""
"""

RETURN = """
"""
from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec=dict(
          before=dict(required=True),
          after=dict(required=True),
          ignore_regexp=dict(required=False)
        )
    )
    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
