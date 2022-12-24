# Ansible Role: Server Workspace (arpanrec.utilities.util_scripts)

Install [Utility Scripts](https://github.com/arpanrec/util_scripts/tree/main/bin) to `{{ rv_util_scripts_bin_dir }}`

## Variables

- Not Applicable

## Example Playbook util_scripts

```yaml
- name: Include Utility Scripts
  ansible.builtin.import_role:
    name: arpanrec.utilities.util_scripts
```

### Testing util_scripts

```bash
molecule test -s role.util_scripts.default
```
