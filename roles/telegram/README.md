# Ansible Role: Telegram (arpanrec.nebula.telegram)

Install [Telegram Desktop](https://desktop.telegram.org/)

## Variables

- `telegram_desktop_rv_install_path`

  - Description: Telegram install path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/telegram_desktop_userapp`

- `telegram_desktop_rv_xdg_icon_path`

  - Description: Telegram icon path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/applications/telegram_desktop_userapps.desktop`

- `telegram_desktop_rv_user_tmp_dir`

  - Description: Telegram install cache and temporary directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/telegram_desktop_userapp`

- `telegram_desktop_rv_version_number`

  - Description:
    - Version number
    - When absent, reads the latest version from [GitHub](https://api.github.com/repos/telegramdesktop/tdesktop/releases/latest)
  - Required: `false`
  - Type: `str`
  - Example: `4.4.1`

- `telegram_desktop_rv_work_directory`
  - Description: Application work directory
  - Required: `false`
  - Type: `str`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/TelegramDesktop`

## Example Playbook Telegram Desktop

```yaml
- name: Include Telegram Desktop
  ansible.builtin.import_role:
    name: arpanrec.nebula.telegram
```

## Testing Telegram Desktop

```bash
molecule test -s role.telegram.default
```
