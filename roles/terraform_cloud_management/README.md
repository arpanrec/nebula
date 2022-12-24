# Ansible Role Terraform Cloud Management

[![Molecule Test](https://github.com/arpanrec/ansible-role-terraform-cloud-management/actions/workflows/test.yml/badge.svg)](https://github.com/arpanrec/ansible-role-terraform-cloud-management/actions/workflows/test.yml) [![Release](https://github.com/arpanrec/ansible-role-terraform-cloud-management/actions/workflows/release.yml/badge.svg)](https://galaxy.ansible.com/arpanrec/terraform_cloud_management)

Ansible Project for managing Terraform Cloud `arpanrec.terraform_cloud_management`

## Role Variables

Variables:

- `rl_tef_api_token`

  - Description: API token for terraform cloud
  - Required: `true`
  - Type: `str`
  - Default: `env TF_PROD_TOKEN`

- `rl_tef_org_name`

  - Description: Name of the terraform cloud organization
  - Required: `true`
  - Type: `str`

- `rl_tef_org_email`

  - Description: Email ID for terraform organization
  - Required: `true`
  - Type: `str`

- `rl_tef_api_collaborator_auth_policy`

  - Description: If two factor is Required
  - Required: `false`
  - Type: `enum` [`password` , `two_factor_mandatory`]

- `rl_tef_workspaces`

  - Description: Workspaces for terraform cloud under organization
  - Required: `false`
  - Type: array[object`rl_tef_workspaces`]

    - `rl_tef_workspace_name`

      - Description: Name of terraform workspace
      - Required: `true`
      - Type: `str`

    - `auto_apply`

      - Description: If `-auto-approve` is applied then state will be applied via the remote
      - Required: `false`
      - Type: `bool`
      - Default: `false`

    - `execution_mode`

      - Description: Which execution mode to use. Valid values are remote, local, and agent. When set to local, the workspace will be used for state storage only. This value must not be specified if operations is specified.
      - Required: `false`
      - Type: `enum` [`remote`, `local`, `agent`]

## Test

```shell
git clone git@github.com:arpanrec/ansible-role-terraform-cloud-management.git arpanrec.terraform_cloud_management
cd arpanrec.terraform_cloud_management
python3 -m pip install --user --upgrade pip
python3 -m pip install --user --upgrade wheel setuptools
python3 -m pip install --user --upgrade virtualenv
virtualenv --python $(readlink -f $(which python3)) venv
source venv/bin/activate
venv/bin/python3 -m pip install -r requirements.txt --upgrade
molecule test
```

## Example Playbook

```yaml
---
- name: Converge
  hosts: all
  tasks:
    - name: Terraform Cloud Management | Include arpanrec.terraform_cloud_management
      ansible.builtin.include_role:
        name: "arpanrec.terraform_cloud_management"
      vars:
        rl_tef_org_name: arpanrec
        rl_tef_org_email: me@arpanrec.com
        rl_tef_api_collaborator_auth_policy: two_factor_mandatory
        rl_tef_workspaces:
          - rl_tef_workspace_name: github-repo-management
            auto_apply: 0
          - rl_tef_workspace_name: test_workspace_2
            auto_apply: 1
            execution_mode: remote
```

## License

`MIT`
