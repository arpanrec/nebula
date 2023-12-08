# Ansible Role Linux Patching (arpanrec.nebula.linux_patching)

Install all latest packages in Debian based systems. also Install basic utility tools for server.
Set timezone, locale, and loopback ip in server

## Role Variables

- `linux_patching_rv_upgrade_existing_packages`

  - Description: If set to `true` Upgrade the existing packages in OS.
  - Required: `false`
  - Default: `true`
  - Type: `bool`

- `linux_patching_rv_packages`

  - Description: Install the packages in the distributions.
  - Required: `false`
  - Default: [ `zip`, `unzip`, `net-tools`, `build-essential`, `tar`, `wget`, `curl`, `ca-certificates`, `sudo`, `systemd`, `telnet`, `gnupg2`, `apt-transport-https`, `lsb-release`, `software-properties-common`, `locales`, `systemd-timesyncd`, `network-manager`, `gnupg2`, `gnupg`, `pigz`, `cron`, `acl`, `ufw`, `vim`, `git`, `fontconfig`, `gtk-update-icon-cache`, `libnss3`, `libatk1.0-0`, `libatk-bridge2.0-0`, `libgtk-3-0`, `bzip2`, `libgbm-dev`, `libglib2.0-dev`, `libdrm-dev`, `libasound2`, `jq`, `zsh`, `libcap2-bin`, `ntfs-3g`, `exfat-fuse`, `vim`, `neovim`, `python3-venv`, `xz-utils`]
  - Type: `list[str]`

- `linux_patching_rv_managed_packages`
  - Description: Install the managed packages in the distributions.
  - Required: `false`
  - Default: []

- `linux_patching_rv_extra_packages`

  - Description: Install extra required the packages.
  - Required: `false`
  - Type: `list[str]`

- `linux_patching_rv_timezone`

  - Description: Set the ZoneTime info in server.
  - Required: `false`
  - Default: `Asia/Kolkata`
  - Type: `str`

- `linux_patching_rv_hostname`

  - Description: Cluster / Public Host name. (Doesn't work with docker)
  - Required: `false`
  - Type: `str`

- `linux_patching_rv_root_ca_pem_content`
  - Description: Organization Root CA certificate.
  - Required: `false`
  - Type: `str`

- `linux_patching_rv_ssh_port`
  - Description: Default SSH Port
  - Required: `false`
  - Type: `int`
  - Default: `22`

## Example Playbook

```yaml
---
- name: Patch Debian System
  become: true
  become_method: su
  any_errors_fatal: true
  ansible.builtin.import_role:
    name: arpanrec.nebula.linux_patching
```

## Testing

```bash
molecule test -s role.linux_patching.default
```
