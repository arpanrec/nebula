# Ansible Role: Bitwarden Desktop (arpanrec.utilities.bitwarden_desktop)

Install bitwarden AppImage [Bitwarden Desktop](https://github.com/bitwarden/clients)

## Variables

- `rv_bitwarden_desktop_version`

  - Description: [Bitwarden Desktop Release](https://github.com/bitwarden/clients/releases?q=Desktop&expanded=true) version like `desktop_*`
  - Default: `v2023.2.0`
  - Type: `str`
  - Required: `false`

- `rv_bitwarden_desktop_install_path`

  - Description: Install directory
  - Default: `{{ pv_ua_user_share_dir }}/bitwarden-desktop`
  - Type: `str`
  - Required: `false`

- `rv_bitwarden_desktop_xdg_icon_path`
  - Description: `.desktop` icon file location
  - Default: `{{ pv_ua_user_share_dir }}/applications/bitwarden-desktop-userapps.desktop`
  - Type: `str`
  - Required: `false`

## Example Playbook Bitwarden Desktop

```yaml
- name: Include bitwarden_desktop
  ansible.builtin.include_role:
    name: arpanrec.utilities.bitwarden_desktop
```

## Testing Bitwarden Desktop

```bash
molecule test -s role.bitwarden_desktop.default
```
