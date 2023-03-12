#!/usr/bin/env python3

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import base64

from ansible.module_utils.basic import AnsibleModule
from hvac import Client

__metaclass__ = type

DOCUMENTATION = r"""
---
module: arpanrec.utilities.vault_sys_generate_root

short_description: Generate Root Token

version_added: "1.0.0"

description: Generate HashiCorp Vault Root Token using Unseal Keys.

options:
    unseal_keys:
        description: List of Required Unseal Keys.
        required: true
        type: list
    vault_addr:
        description: Vault endpoint
        required: false
        type: bool
        default: "http://localhost:8200"
    vault_client_cert:
        description: Hashicorp Vault Mutual TLS Client Certificate Path
        required: false
        type: str
    vault_client_key:
        description: Hashicorp Vault Mutual TLS Client Key Path
        required: false
        type: str
    vault_capath:
        description: Hashicorp Vault CA Path
        required: false
        type: str
    cancel_root_generation:
        description: Cancel if already in progress
        required: false
        type: bool
        default: false
    calculate_new_root:
        description: Regenerate vault root token, with base64 decode the encoded_root_token XOR with bytes of OTP
        required: false
        type: bool
        default: false
author:
    - Arpan Mandal (mailto:arpan.rec@gmail.com)
"""

EXAMPLES = r"""
# Pass in a message
- name: recreate root token
  arpanrec.utilities.vault_sys_generate_root:
    unseal_keys:
        [
        "xxxxx",
        "yyyyy",
        "zzzzz",
        ]
    vault_addr: https://vault.com:8200
    vault_client_cert: "vault_client_auth.crt"
    vault_client_key: "vault_client_auth.key"
    vault_capath: "root_ca_certificate.crt"
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
encoded_root_token:
    description: Base64 ascii encoded root token
    type: str
    returned: always
otp:
    description: OTP
    type: str
    returned: always
new_root:
    description: ((OTP bytes) XOR (base64 ascii decode of encoded_root_token))
    type: str
    returned: if calculate_new_root
"""


def root_gen(
    unseal_keys=None,
    vault_addr=None,
    vault_client_cert=None,
    vault_client_key=None,
    vault_capath=None,
    cancel_root_generation: bool = False,
    calculate_new_root: bool = False,
):

  result = {}

  vault_client_config = dict(url=vault_addr)
  if vault_capath:
    vault_client_config["verify"] = vault_capath
  if vault_client_cert:
    vault_client_config["cert"] = (vault_client_cert, vault_client_key)

  vault_client = Client(**vault_client_config)

  read_root_generation_progress_response = (
      vault_client.sys.read_root_generation_progress()
  )
  required_num_of_unseal_keys = read_root_generation_progress_response["required"]
  provided_num_of_unseal_keys = len(unseal_keys)
  if provided_num_of_unseal_keys < required_num_of_unseal_keys:
    return {
        "error": f"Required unseal keys {required_num_of_unseal_keys}, but provided {provided_num_of_unseal_keys}",
        "result": result,
    }

  if read_root_generation_progress_response["started"]:
    if cancel_root_generation:
      vault_client.sys.cancel_root_generation()
      result["changed"] = True
    else:
      return {"error": "root generation already in progress", "result": result}

  start_generate_root_response = vault_client.sys.start_root_token_generation()

  result["changed"] = True
  otp = start_generate_root_response["otp"]
  nonce = start_generate_root_response["nonce"]
  result["otp"] = otp
  for unseal_key in unseal_keys:
    generate_root_response = vault_client.sys.generate_root(
        key=unseal_key,
        nonce=nonce,
    )

    if generate_root_response["progress"] == generate_root_response["required"]:
      break

  result["generate_root_response"] = generate_root_response
  encoded_root_token = generate_root_response["encoded_root_token"]

  if not encoded_root_token:
    return {"error": "Encoded root token not found", "result": result}

  result["encoded_root_token"] = encoded_root_token

  if calculate_new_root:
    _root_token = base64.b64decode(bytearray(encoded_root_token, "ascii") + b"==")
    _otp_bytes = bytearray(otp, "ascii")
    _final_root_token_bytes = bytearray()
    for i, j in zip(_root_token, _otp_bytes):
      _final_root_token_bytes.append(i ^ j)
    result["new_root"] = str(_final_root_token_bytes.decode("utf-8"))
  return {"result": result}


def run_module():
  # define available arguments/parameters a user can pass to the module
  module_args = dict(
      unseal_keys=dict(type="list", elements="str", required=True, no_log=True),
      vault_addr=dict(type="str", required=False, default="http://localhost:8200"),
      vault_client_cert=dict(type="str", required=False),
      vault_client_key=dict(type="str", required=False),
      vault_capath=dict(type="str", required=False),
      cancel_root_generation=dict(type="bool", required=False, default=False),
      calculate_new_root=dict(type="bool", required=False, default=False),
  )

  module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

  root_gen_result = root_gen(
      unseal_keys=module.params["unseal_keys"],
      vault_addr=module.params["vault_addr"],
      vault_client_cert=module.params["vault_client_cert"],
      vault_client_key=module.params["vault_client_key"],
      vault_capath=module.params["vault_capath"],
      cancel_root_generation=module.params["cancel_root_generation"],
      calculate_new_root=module.params["calculate_new_root"],
  )

  if "error" in root_gen_result.keys():
    return module.fail_json(
        msg=root_gen_result["error"], **root_gen_result["result"]
    )

  module.exit_json(**root_gen_result["result"])


def main():
  run_module()


if __name__ == "__main__":
  main()
