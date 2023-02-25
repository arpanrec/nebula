# Ansible Role: NewVIM (arpanrec.utilities.nvim)

Install [NeoVIM](https://neovim.io/) with setup with vim plug coc python

## Variables

- `rv_nvim_version`

  - Description: Version of [NeoVIM GitHub](https://github.com/neovim/neovim/releases).
  - Type: `str`
  - Required: `false`
  - Default: `v0.8.1`

- `rv_nvim_nodejs_install_path`

  - Description: NodeJS dependency install path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/node`

- `rv_nvim_user_tmp_dir`

  - Description: Install cache and temporary directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.tmp/nvim`

- `rv_nvim_config_dir`

  - Description: Neovim config directory.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.config/nvim`

- `rv_nvim_exec_path`

  - Description: Neovim executable path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/bin/nvim`

- `rv_nvim_install_path`

  - Description: Neovim Install path.
  - Type: `str`
  - Required: `false`
  - Default: `{{ ansible_facts.user_dir }}/.local/share/nvim`

## Example Playbook NeoVIM

```yaml
- name: Include NeoVIM
  ansible.builtin.include_role:
    name: arpanrec.utilities.nvim
```

## Testing NeoVIM

```bash
molecule test -s role.nvim.default
```
