# Ansible Role User Add (arpanrec.utilities.user_add)

Create a user and add it to sudoers.d

## Role Variables

- `user_add_rv_user_primary_group`

  - Type: `String`
  - Required: `false`
  - Default: `{{ user_add_rv_username }}`
  - Description: Group Name : Primary Group of the user

- `user_add_rv_user_primary_gid`

  - Type: `int`
  - Required: `false`
  - Default: `omit`
  - Description: Group ID : GID for primary group

- `user_add_rv_username`

  - Type: `String`
  - Required: `true`
  - Description: Username

- `user_add_rv_uid`

  - Type: `int`
  - Required: `false`
  - Default: `omit`
  - Description: User ID : UID

- `user_add_rv_password`

  - Type: `String`
  - Required: `false`
  - Description: Clear text password for the user

- `user_add_rv_user_extra_groups`

  - Type: `List<String>`
  - Required: `false`
  - Description: Groups : Extra groups for user

- `user_add_rv_ssh_access_public_key_content_list`

  - Type: `list<str>`
  - Required: `false`
  - Description: Public key for remote ssh access

- `user_add_rv_user_nopasswd_commands`

  - Type: `List<String>`
  - Required: `false`
  - Description: Commands user will be able to run without password

- `user_add_rv_user_default_shell`

  - Type: `str`
  - Required: `false`
  - Default: `/bin/bash`
  - Description: Default shell for the User

- `user_add_rv_user_home_dir`
  - Type: `str`
  - Required: `false`
  - Description: Path to home

## Example Playbook

```yaml
- name: Add application user
  import_role:
    name: arpanrec.utilities.user_add
  vars:
    user_add_rv_username: "arpan"
    user_add_rv_ssh_access_public_key_content_list: ["ssh-rsa yc2E"]
```

## Testing

Prerequisite: `docker`, `python3-venv`

```bash
molecule test -s role.user_add.default
```

## License

`MIT`
