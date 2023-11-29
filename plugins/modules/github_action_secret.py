#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ansible Module for adding github action secret.
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

from base64 import b64encode

import requests
from ansible.module_utils.basic import AnsibleModule
from nacl import encoding, public

# pylint: disable=C0103
__metaclass__ = type


DOCUMENTATION = r"""
---
module: github_action_secret

short_description: Create Update Delete Github Action Secret

version_added: "1.0.0"

description: Create Update Delete Github Action Secret.

options:
  api_ep:
    description: Rest Api endpoint
    required: false
    type: str
    default: "https://api.github.com"
  pat:
    description: Github PAT.
    required: true
    type: str
  owner:
    description:
      - Owner Of the repository
      - When organization and owner both are missing, this value will be set as the owner of PAT
      - mutually exclusive with organization
    required: false
    type: str
  organization:
    description:
      - organization of the repository
      - If repository is missing then the secret wil be added to organization secret
    required: false
    type: str
  unencrypted_secret:
    description: Plain text action secret
    required: false
    type: str
  name:
    description: Name of the secret
    required: true
    type: str
  repository:
    description: Name of the github repository.
    required: false
    type: str
  state:
    description: State of the secret.
    required: false
    type: str
    choices: ["present", "absent"]
    default: present
  visibility:
    description: Mandatory for organization secrets
    choices: ["private", "all", "selected"]
    type: str
    required: false
author:
  - Arpan Mandal (mailto:arpan.rec@gmail.com)
"""

EXAMPLES = r"""
- name: Create or Update a repository secret
  github_action_secret:
    api_ep: "https://api.github.com"
    pat: "{{ lookup('ansible.builtin.env', 'GH_PROD_API_TOKEN') }}"
    unencrypted_secret: "supersecret"
    repository: "github_master_controller"
    name: "ENV_SECRET1"

- name: Create or Update a organization secret
  github_action_secret:
    api_ep: "https://api.github.com"
    pat: "{{ lookup('ansible.builtin.env', 'GH_PROD_API_TOKEN') }}"
    unencrypted_secret: "supersecret"
    name: "ENV_SECRET"
    organization: arpanrec
    state: present
    visibility: all

- name: Delete a repository secret
  github_action_secret:
    api_ep: "https://api.github.com"
    pat: "{{ lookup('ansible.builtin.env', 'GH_PROD_API_TOKEN') }}"
    repository: "github_master_controller"
    name: "ENV_SECRET"
    state: absent
"""

RETURN = r"""
public_key:
  description: Public Key of the repository
  type: str
  returned: if state == present
public_key_id:
  description: Public Key id of the repository
  type: str
  returned: if state == present
secret:
  description: Encrypted secret
  type: str
  returned: if state == present
"""


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def crud(
    pat=None,
    owner=None,
    unencrypted_secret=None,
    name=None,
    repository=None,
    api_ep=None,
    organization=None,
    state=None,
    visibility=None,
) -> dict:
    """
    Performs Create, Read, Update, and Delete (CRUD) operations.

    This function is responsible for performing CRUD operations on GitHub Action Secrets based on the provided parameters.

    Parameters:
        api_ep (str): The endpoint of the GitHub API. Defaults to "https://api.github.com".
        pat (str): The Personal Access Token (PAT) for the GitHub API. Required.
        owner (str): The owner of the repository. Optional.
        organization (str): The organization of the repository. Optional.
        unencrypted_secret (str): The plain text action secret. Optional.
        name (str): The name of the secret. Required.

    Returns:
        dict: A dictionary containing the results of the CRUD operation.
    """

    result = {"changed": False, "updated": False, "created": False, "deleted": False}
    create_update_data = {}
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"token {pat}"}
    if owner and not repository:
        result["error"] = "'repository' is mandatory when 'owner' is set"
        return result

    if state not in ("present", "absent"):
        result["error"] = f"state should be either present or absent, {state}"
        return result

    if (not owner) and (not repository) and (organization) and visibility not in ["private", "all", "selected"]:
        result["error"] = "visibility should in 'private', 'all', 'selected'"
        return result

    if owner and repository:
        public_key_ep = f"{api_ep}/repos/{owner}/{repository}/actions/secrets/public-key"
        secret_ep = f"{api_ep}/repos/{owner}/{repository}/actions/secrets/{name}"
    elif (not owner) and (repository) and (not organization):
        owner = requests.get(f"{api_ep}/user", headers=headers, timeout=30).json()["login"]
        public_key_ep = f"{api_ep}/repos/{owner}/{repository}/actions/secrets/public-key"
        secret_ep = f"{api_ep}/repos/{owner}/{repository}/actions/secrets/{name}"
    elif (not owner) and (not repository) and (organization):
        public_key_ep = f"{api_ep}/orgs/{organization}/actions/secrets/public-key"
        secret_ep = f"{api_ep}/orgs/{organization}/actions/secrets/{name}"
        create_update_data["visibility"] = visibility
    elif (not owner) and (repository) and (organization):
        public_key_ep = f"{api_ep}/repos/{organization}/{repository}/actions/secrets/public-key"
        secret_ep = f"{api_ep}/repos/{organization}/{repository}/actions/secrets/{name}"

    if state == "present":
        public_key_ep_res = requests.get(public_key_ep, headers=headers, timeout=30)
        if public_key_ep_res.status_code == 200:
            result["public_key"] = public_key_ep_res.json().get("key")
            result["public_key_id"] = public_key_ep_res.json().get("key_id")
        else:
            result["error"] = {
                "response": public_key_ep_res.json(),
                "status": public_key_ep_res.status_code,
            }
            return result

        if unencrypted_secret:
            secret = encrypt(public_key=result["public_key"], secret_value=unencrypted_secret)
        result["secret"] = secret
        create_update_data["encrypted_value"] = secret
        create_update_data["key_id"] = result["public_key_id"]
        secret_ep_response = requests.put(secret_ep, headers=headers, timeout=30, json=create_update_data)
        if secret_ep_response.status_code == 204:
            result["updated"] = True
            result["changed"] = True
        elif secret_ep_response.status_code == 201:
            result["changed"] = True
            result["created"] = True
        else:
            result["error"] = {
                "response": secret_ep_response.json(),
                "status": secret_ep_response.status_code,
            }
            return result
    if state == "absent":
        delete_response = requests.delete(secret_ep, headers=headers, timeout=30)
        if delete_response.status_code == 204:
            result["changed"] = True
            result["deleted"] = True
        elif delete_response.status_code == 404:
            pass
        else:
            result["error"] = (
                {
                    "response": delete_response.json(),
                    "status": delete_response.status_code,
                },
            )
            return result
    return result


def run_module():
    """
    Ansible main module
    """
    # define available arguments/parameters a user can pass to the module
    module_args = {
        "api_ep": {"type": "str", "required": False, "default": "https://api.github.com"},
        "pat": {"type": "str", "required": True, "no_log": True},
        "owner": {"type": "str", "required": False},
        "organization": {"type": "str", "required": False},
        "unencrypted_secret": {"type": "str", "required": False, "no_log": True},
        "name": {"type": "str", "required": True},
        "repository": {"type": "str", "required": False},
        "state": {"type": "str", "required": False, "default": "present", "choices": ["present", "absent"]},
        "visibility": {"type": "str", "required": False, "choices": ["private", "all", "selected"]},
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        mutually_exclusive=[
            ("owner", "organization"),
            ("unencrypted_secret", "secret"),
            ("owner", "visibility"),
        ],
        required_one_of=[
            ("repository", "organization"),
        ],
        required_if=[
            ("state", "present", (["unencrypted_secret"]), False),
        ],
    )

    github_update_response = crud(
        api_ep=module.params["api_ep"],
        pat=module.params["pat"],
        owner=module.params["owner"],
        unencrypted_secret=module.params["unencrypted_secret"],
        name=module.params["name"],
        repository=module.params["repository"],
        organization=module.params["organization"],
        state=module.params["state"],
        visibility=module.params["visibility"],
    )

    if "error" in github_update_response:
        return module.fail_json(msg=github_update_response["error"], **github_update_response)

    module.exit_json(**github_update_response)


def main():
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
