# Ansible Role: Terraform (arpanrec.utilities.terraform)

## Terraform

Install Terraform in user space

## Variable

- `rv_terraform_install_path`

  - Description: Install path for terraform.
  - Default: `"{{ ansible_facts.user_dir }}/.local/bin"`
  - Required: `false`
  - Type: `str`

- `rv_terraform_version`

  - Description: Release version.
  - Default: `v16.19.0`
  - Required: `false`
  - Type: `str`

- `rv_terraform_tmp_install_cache_dir`
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
