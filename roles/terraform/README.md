# Ansible Role: Terraform (arpanrec.utilities.terraform)

## Terraform

Install Terraform in user space

## Variable

- `terraform_rv_install_path`

  - Description: Install path for terraform.
  - Default: `"{{ ansible_facts.user_dir }}/.local/bin"`
  - Required: `false`
  - Type: `str`

- `terraform_rv_version`

  - Description:
    - Release version.
    - Get latest release from [Github releases](https://api.github.com/repos/hashicorp/terraform/releases/latest)
    - Example format `1.0.9`
  - Required: `false`
  - Type: `str`

- `terraform_rv_tmp_install_cache_dir`
  - Description: Cache install directory.
  - Default: `"{{ ansible_facts.user_dir }}/.tmp/terraform"`
  - Required: `false`
  - Type: `str`

### Example Playbook Terraform

```yaml
- name: Include Terraform
  ansible.builtin.import_role:
    name: arpanrec.utilities.terraform
```

### Testing Terraform

```bash
molecule test -s role.terraform.default
```
