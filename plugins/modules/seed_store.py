#!/usr/bin/env python3
"""
Ansible Module for adding / updating / deleting init store
"""

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from psychicoctowinner.seed_store import store

# pylint: disable=C0103
__metaclass__ = type

DOCUMENTATION = r"""
---
module: seed_store
short_description: Add / Update / Delete a variable in Init store bucket
description:
  - Add / Update / Delete a variable in a Init store bucket
author: "Arpan Mandal (@arpanrec)"
options:
  endpoint:
    description: Init Store endpoint
    required: true
  credential:
    description: Init Store credential
    required: true
  key:
    description: Name of the variable to be stored
    required: true
  value:
    description: Value of the variable to be stored
    required: false
  value1:
    description: Value of the variable to be stored
    required: false
  mark_for_delete:
    description: Delete the variable
    required: false
    default: false
    type: bool
  behavior_on_not_found:
    description: Behavior when the variable is not found
    required: false
    default: None
    choices: [None, Error, Empty]
    type: str
"""


# pylint: disable=C0114,C0116,R1735,W0718
def run_module():
    module_args = {
        "endpoint": {"type": "str", "required": True},
        "credential": {"type": "str", "required": True, "no_log": True},
        "key": {"type": "str", "required": True},
        "value": {"type": "str", "required": False},
        "mark_for_delete": {"type": "bool", "required": False, "default": False},
        "behavior_on_not_found": {
            "type": "str",
            "required": False,
            "default": "None",
            "choices": ["None", "Error", "Empty"],
        },
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    try:
        changed = False
        value, is_success = store(
            key=module.params["key"],
            value=module.params["value"],
            endpoint=module.params["endpoint"],
            credential=module.params["credential"],
            mark_for_delete=module.params["mark_for_delete"],
            behavior_on_not_found=module.params["behavior_on_not_found"],
        )

        if module.params["value"] and is_success:
            changed = True

        if module.params["mark_for_delete"] and is_success:
            changed = True

        module.exit_json(**{"value": value, "is_success": is_success, "changed": changed})
    except Exception as e:
        module.fail_json(msg=str(e))


def main():
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
