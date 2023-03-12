#!/usr/bin/env python3

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.hashicorp_tfe_core import crud

__metaclass__ = type


DOCUMENTATION = r"""
---
module: arpanrec.utilities.terraform_cloud_workspace

short_description: Create Update terraform cloud workspace

version_added: "1.0.0"

description: Create Update terraform cloud workspace.

options:
    hostname:
        description: Terraform Cloud Hostname.
        required: false
        type: str
        default: app.terraform.io
    token:
        description: Terraform Cloud Access Token.
        required: true
        type: str
    organization:
        description: Name of terraform cloud organization
        required: true
        type: str
    organization_attributes:
        description:
            - Attributes of terraform cloud organization
            - Find the list of attributes: `https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations\#update-an-organization`
        required: false
        type: dict
    workspace:
        description: Name of terraform workspace
        required: true
        type: str
    workspace_attributes:
        description:
            - Attributes of terraform cloud organization
            - Find the list of attributes: `https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces\#update-a-workspace`
        required: false
        type: bool
author:
    - Arpan Mandal (mailto:arpan.rec@gmail.com)
"""

EXAMPLES = r"""
# Prepare Terraform cloud
- name: Prepare Terraform cloud
  arpanrec.utilities.terraform_cloud_workspace:
    token: "xxxxxxxxxxxxx"
    organization: testorg
    organization_attributes:
        email: user@email.com
        "collaborator-auth-policy": "two_factor_mandatory"
    workspace: "vault_client_auth"
    workspace_attributes:
        "allow-destroy-plan": true
        "auto-apply": true
        "execution-mode": "local"
"""

RETURN = r"""
These are examples of possible return values, and in general should use other names for return values.
organization:
    description: Details of terraform cloud organization.
    type: dict
    returned: always
workspace:
    description: Details of terraform cloud workspace.
    type: dict
    returned: always
"""


def run_module():
  # define available arguments/parameters a user can pass to the module
  module_args = dict(
      hostname=dict(required=False, default="app.terraform.io"),
      token=dict(type="str", required=True, no_log=True),
      organization=dict(type="str", required=True),
      organization_attributes=dict(type="dict", required=False),
      workspace=dict(type="str", required=True),
      workspace_attributes=dict(type="dict", required=False),
  )

  module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=False,
  )

  tfe_response = crud(
      hostname=module.params["hostname"],
      token=module.params["token"],
      organization=module.params["organization"],
      organization_attributes=module.params["organization_attributes"],
      workspace=module.params["workspace"],
      workspace_attributes=module.params["workspace_attributes"],
  )

  if "error" in tfe_response.keys():
    return module.fail_json(msg=tfe_response["error"], **tfe_response)

  module.exit_json(**tfe_response)


def main():
  run_module()


if __name__ == "__main__":
  main()
