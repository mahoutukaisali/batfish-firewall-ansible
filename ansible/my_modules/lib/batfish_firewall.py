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
  - Test wether ACL is properly configured or not
options:
  src:
    description:
      - Address of source.
  dest:
    description:
      - Address of destination.
  protocol:
    description:
      - Protocol name
  condition:
    description:
      - The condition which one shoud be 'permit' or 'deny'.
  nodes:
    description:
      - node name which has the target ACL
  acl_name:
    description:
      - ACL name which is the target ACL name
"""

EXAMPLES = r"""
"""

RETURN = """
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils._text import to_bytes, to_native

def main():

  module = AnsibleModule(
    # not checking because of daisy chain to file module
    argument_spec = dict(
        src = dict(required=False),
        dest = dict(required=False),
        protocol = dict(required=False),
        condition = dict(required=False),
        node = dict(required=True),
        acl_name = dict(required=True)
    ),
    add_file_common_args=True,
    supports_check_mode=False,
  )

  module.exit_json(changed=False)

if __name__ == '__main__':
    main()
