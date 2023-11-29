#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module provides functionality for generating a root token for HashiCorp Vault using unseal keys.

It uses the HashiCorp Vault API Client (hvac) to interact with the Vault system. The module takes a list of unseal keys as input,
which are used to generate a new root token. The new token is not returned by the module, but is instead stored securely within the Vault system.

The module also provides options for specifying the Vault address, client certificate and key, and CA path. Additionally, it allows for the cancellation of the root generation process and the calculation of a new root.

This module is part of the arpanrec.utilities collection.

Author:
    Arpan Mandal (arpan.rec@gmail.com)
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import base64

from ansible.module_utils.basic import AnsibleModule
from hvac import Client

# pylint: disable=C0103
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
    unseal_keys: list,
    vault_addr=None,
    vault_client_cert=None,
    vault_client_key=None,
    vault_ca_path=None,
    cancel_root_generation: bool = False,
    calculate_new_root: bool = False,
):
    """
    Generates a new root token for the Vault system.

    This function initiates the process of generating a new root token for the Vault system.
    The new token is not returned by this function, but is instead stored securely within the Vault system.

    Raises:
        VaultError: If there is an issue with the Vault system that prevents the generation of a new root token.

    Returns:
        None
    """

    result = {}

    vault_client_config = dict(url=vault_addr)
    if vault_ca_path:
        vault_client_config["verify"] = vault_ca_path
    if vault_client_cert:
        vault_client_config["cert"] = (vault_client_cert, vault_client_key)

    vault_client = Client(**vault_client_config)

    read_root_generation_progress_response = vault_client.sys.read_root_generation_progress()
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
    """
    Executes the main functionality of the module.

    This function takes a set of parameters to configure the Vault system,
    including unseal keys, Vault address, client certificate and key,
    and options to cancel root generation and calculate a new root.

    Parameters:
        unseal_keys (list of str): The unseal keys for the Vault system. Required.
        vault_addr (str): The address of the Vault system. Defaults to "http://localhost:8200".
        vault_client_cert (str): The client certificate for the Vault system. Optional.
        vault_client_key (str): The client key for the Vault system. Optional.
        vault_capath (str): The CA path for the Vault system. Optional.
        cancel_root_generation (bool): Whether to cancel the root generation process. Defaults to False.
        calculate_new_root (bool): Whether to calculate a new root. Defaults to False.

    Returns:
        dict: A dictionary containing the results of the module execution.
    """

    module_args = {
        "unseal_keys": {"type": "list", "elements": "str", "required": True, "no_log": True},
        "vault_addr": {"type": "str", "required": False, "default": "http://localhost:8200"},
        "vault_client_cert": {"type": "str", "required": False},
        "vault_client_key": {"type": "str", "required": False},
        "vault_capath": {"type": "str", "required": False},
        "cancel_root_generation": {"type": "bool", "required": False, "default": False},
        "calculate_new_root": {"type": "bool", "required": False, "default": False},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    root_gen_result = root_gen(
        unseal_keys=module.params["unseal_keys"],
        vault_addr=module.params["vault_addr"],
        vault_client_cert=module.params["vault_client_cert"],
        vault_client_key=module.params["vault_client_key"],
        vault_ca_path=module.params["vault_capath"],
        cancel_root_generation=module.params["cancel_root_generation"],
        calculate_new_root=module.params["calculate_new_root"],
    )

    if "error" in root_gen_result:
        return module.fail_json(msg=root_gen_result["error"], **root_gen_result["result"])

    module.exit_json(**root_gen_result["result"])


def main():
    """
    Main function for the module.
    """

    run_module()


if __name__ == "__main__":
    main()
