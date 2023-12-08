# Ansible Role: Bitwarden CLI (arpanrec.nebula.bw)

## Bitwarden CLI

Install [Bitwarden ClI](https://www.npmjs.com/package/@bitwarden/cli)

Variables:

- `bw_cli_rv_version`

  - Description: Version of [Bitwarden ClI](https://www.npmjs.com/package/@bitwarden/cli) npm module.
  - Type: `str`
  - Required: `false`
  - Default: `2023.10.0`

- `bw_cli_rv_node_dependency_bin_dir`

  - Description: NPM Directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/node/bin`

- `bw_bws_version_tag`
  - Description:
    - Version of [Bitwarden BWS SDK ClI](https://github.com/bitwarden/sdk/releases).
    - Default Get latest release name from [github](https://api.github.com/repos/bitwarden/sdk/releases/latest)
  - Type: `str`
  - Required: `false`
  - Example: `0.3.1`

- `bw_bws_bin_dir`
  - Description: Directory to install BWS
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/bin`

- `bw_bws_tmp_dir`
  - Description: Directory to temporary download BWS.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/bw`

### Example Playbook Bitwarden CLI

```yaml
- name: Include Bitwarden CLI
  ansible.builtin.import_role:
    name: arpanrec.nebula.bw
```

### Testing Bitwarden CLI

```bash
molecule test -s role.bw.default
```
