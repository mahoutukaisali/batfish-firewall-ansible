#!/usr/bin/python
# -*- coding: utf-8 -*-
# import module snippets
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils._text import to_bytes, to_native

def main():

  module = AnsibleModule(
    # not checking because of daisy chain to file module
    argument_spec = dict(
        src = dict(required=False),
        dest = dict(required=False),
        protocol = dict(required=False)
    ),
    add_file_common_args=True,
    supports_check_mode=True,
  )

module.exit_json(**res_args)

if __name__ == '__main__':
    main()