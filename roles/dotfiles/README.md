# Ansible Role: dotfiles (arpanrec.utilities.dotfiles)

Track your dotfiles from [GitHub](https://github.com/arpanrecme/dotfiles). You can track these files with below command. (Follow the git commands for reference)

```shell
config pull # To pull the changes
config add <filepath> # Track new files/Changes
config commit -m"New Config added/Changed" # Track new files
config push # Push to remote
```

## Variables

```yaml
options:
  dotfiles_rv_user_home_dir:
    description: User home directory.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}"
  dotfiles_rv_git_remote:
    description: Git remote.
    required: false
    type: str
    default: https://github.com/arpanrec/dotfiles
  dotfiles_rv_git_version:
    description: Git Branch.
    required: false
    type: str
    default: main
  dotfiles_rv_bare_relative_dir:
    description: "Git bare directory in {{ dotfiles_rv_user_home_dir }}."
    required: false
    type: str
    default: ".dotfiles"
```

## Example Playbook dotfiles

```yaml
---
- name: Dotfiles
  hosts: all
  gather_facts: false
  become: false
  any_errors_fatal: true
  roles:
    - name: arpanrec.utilities.dotfiles
```
