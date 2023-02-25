# Ansible Role: Postman (arpanrec.utilities.postman)

Install [postman](https://www.postman.com/)

## Variables

- `rv_postman_install_path`

  - Description: Postman install path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/Postman`

- `rv_postman_xdg_icon_path`

  - Description: Desktop icon path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/applications/postman-userapps.desktop`

- `rv_postman_user_tmp_dir`
  - Description: Install cache and temporary directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/postman_app`

### Example Playbook postman

```yaml
- name: Include postman
  ansible.builtin.include_role:
    name: arpanrec.utilities.postman
```

### Testing postman

```bash
molecule test -s role.postman.default
```
