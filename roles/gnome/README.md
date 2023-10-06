# Ansible Role: Gnome Desktop (arpanrec.utilities.gnome)

Install Gnome Extensions and setup

## Variables

- `gnome_rv_extension_list`

  - Description: List of Extensions
  - Type: Array
    `[
    - {`name`:`{{ name }}`,`id`:`{{ id }}`}
      ]`
  - Default:
    - name: "user-themes"
      id: 19
    - name: "AppIndicator and KStatusNotifierItem Support"
      id: 615
    - name: "workspace-indicator"
      id: 21
    - name: "applications-menu"
      id: 6
    - name: "vitals"
      id: 1460

- `gnome_rv_user_share_dir`

  - Description:
    - User share directory.
    - Extensions will be install in `{{ gnome_rv_user_share_dir }}/gnome-shell/extensions/<uuid>`
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share`

- `gnome_rv_user_cache_tmp_dir`
  - Description: Install cache and temporary directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/gnome_ansible`

## Example Playbook Gnome

```yaml
- name: Include Gnome
  ansible.builtin.import_role:
    name: arpanrec.utilities.gnome
```

## Testing Gnome

```bash
molecule test -s role.gnome.default
```
