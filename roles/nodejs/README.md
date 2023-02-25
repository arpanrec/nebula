# Ansible Role: NodeJS (arpanrec.utilities.nodejs)

## NodeJS

Install NodeJS in user space

## Variable

- `rv_nodejs_install_path`

  - Description: Install path for nodejs.
  - Default: `"{{ ansible_facts.user_dir }}/.local/share/node"`
  - Required: `false`
  - Type: `str`

- `rv_nodejs_version`

  - Description: Release version.
  - Default: `v16.19.0`
  - Required: `false`
  - Type: `str`

- `rv_nodejs_tmp_install_cache_dir`
  - Description: Cache install directory.
  - Default: `"{{ ansible_facts.user_dir }}/.tmp/nodejs"`
  - Required: `false`
  - Type: `str`

### Example Playbook NodeJS

```yaml
- name: Include NodeJS
  ansible.builtin.include_role:
    name: arpanrec.utilities.nodejs
```

### Testing NodeJS

```bash
molecule test -s role.nodejs.default
```
