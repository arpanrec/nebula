# Ansible Role: Mattermost Desktop (arpanrec.utilities.mattermost_desktop)

Install [Mattermost Desktop](https://github.com/mattermost/desktop/releases)

## Variables

- `pv_ua_mm_release_version`

  - Description: Release Version of [Mattermost Desktop](https://github.com/mattermost/desktop/releases)
  - Type: `str`
  - Required: `false`
  - Default: [Latest Github Release](https://api.github.com/repos/mattermost/desktop/releases/latest).tag_name
  - Example: `v5.1.0`

- `rv_mattermost_desktop_user_tmp_dir`

  - Description: Install cache directory
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/mattermost_desktop`

- `rv_mattermost_desktop_install_path`

  - Description: Install directory
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/mattermost-desktop`

- `rv_mattermost_desktop_xdg_icon_path`
  - Description: Linux desktop icon path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/applications/mattermost-desktop-userapps.desktop`

## Example Playbook Mattermost Desktop

```yaml
- name: Include bitwarden_desktop
  ansible.builtin.include_role:
    name: arpanrec.utilities.mattermost_desktop
```

## Testing Mattermost Desktop

```bash
molecule test -s role.mattermost_desktop.default
```
