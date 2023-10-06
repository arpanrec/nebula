# Ansible Role: Bitwarden CLI (arpanrec.utilities.bw)

## Bitwarden CLI

Install [Bitwarden ClI](https://www.npmjs.com/package/@bitwarden/cli)

Variables:

- `bw_cli_rv_version`

  - Description: Version of [Bitwarden ClI](https://www.npmjs.com/package/@bitwarden/cli) npm module.
  - Type: `str`
  - Required: `false`
  - Default: `2023.3.0`

- `bw_cli_rv_node_dependency_bin_dir`

  - Description: NPM Directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/node/bin`

### Example Playbook Bitwarden CLI

```yaml
- name: Include Bitwarden CLI
  ansible.builtin.import_role:
    name: arpanrec.utilities.bw
```

### Testing Bitwarden CLI

```bash
molecule test -s role.bw.default
```
