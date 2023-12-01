"""
This module provides functionality for creating and updating a Terraform Cloud workspace.

It uses the HashiCorp Terraform Cloud API to interact with the Terraform Cloud system. The module takes a hostname, access token, organization name, workspace name, and optional organization and workspace attributes as input.

The module is capable of creating a new workspace if it does not exist, or updating an existing workspace with new attributes.
The updated or newly created workspace is not returned by the module, but is instead stored within the Terraform Cloud system.

This module is part of the arpanrec.utilities collection.

Author:
    Arpan Mandal (arpan.rec@gmail.com)
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from psychicoctowinner.hashicorp_tfe_core import crud

# pylint: disable=C0103
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
      - Find the list of attributes: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/organizations\#update-an-organization
    required: false
    type: dict
  workspace:
    description: Name of terraform workspace
    required: true
    type: str
  workspace_attributes:
    description:
      - Attributes of terraform cloud organization
      - Find the list of attributes: https://developer.hashicorp.com/terraform/cloud-docs/api-docs/workspaces\#update-a-workspace
    required: false
    type: bool
author:
  - Arpan Mandal (mailto:arpan.rec@gmail.com)

"""

EXAMPLES = r"""
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
    """
    Executes the main functionality of the module.

    This function is responsible for creating, updating, or deleting a Terraform Cloud workspace based on the provided parameters.

    Parameters:
        hostname (str): The hostname of the Terraform Cloud instance. Defaults to "app.terraform.io".
        token (str): The access token for the Terraform Cloud instance. Required.
        organization (str): The name of the organization in Terraform Cloud. Required.
        organization_attributes (dict): The attributes for the organization in Terraform Cloud. Optional.
        workspace (str): The name of the workspace in Terraform Cloud. Required.
        workspace_attributes (dict): The attributes for the workspace in Terraform Cloud. Optional.

    Returns:
        dict: A dictionary containing the results of the module execution.
    """

    module_args = {
        "hostname": {"required": False, "default": "app.terraform.io"},
        "token": {"type": "str", "required": True, "no_log": True},
        "organization": {"type": "str", "required": True},
        "organization_attributes": {"type": "dict", "required": False},
        "workspace": {"type": "str", "required": True},
        "workspace_attributes": {"type": "dict", "required": False},
    }

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
    """
    Main function for the module.
    """

    run_module()


if __name__ == "__main__":
    main()
