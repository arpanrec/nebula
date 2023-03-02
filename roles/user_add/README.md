# Ansible Role User Add (arpanrec.utilities.user_add)

Create a user and add it to sudoers.d

## Role Variables

- `rv_user_add_user_primary_group`

  - Type: `String`
  - Required: `false`
  - Default: `{{ rv_user_add_username }}`
  - Description: Group Name : Primary Group of the user

- `rv_user_add_user_primary_gid`

  - Type: `int`
  - Required: `false`
  - Default: `omit`
  - Description: Group ID : GID for primary group

- `rv_user_add_username`

  - Type: `String`
  - Required: `true`
  - Description: Username

- `rv_user_add_uid`

  - Type: `int`
  - Required: `false`
  - Default: `omit`
  - Description: User ID : UID

- `rv_user_add_password`

  - Type: `String`
  - Required: `false`
  - Description: Clear text password for the user

- `rv_user_add_user_extra_groups`

  - Type: `List<String>`
  - Required: `false`
  - Description: Groups : Extra groups for user

- `rv_user_add_ssh_access_public_key_content_list`

  - Type: `list<str>`
  - Required: `false`
  - Description: Public key for remote ssh access

- `rv_user_add_user_nopasswd_commands`

  - Type: `List<String>`
  - Required: `false`
  - Description: Commands user will be able to run without password

- `rv_user_add_user_default_shell`

  - Type: `str`
  - Required: `false`
  - Default: `/bin/bash`
  - Description: Default shell for the User

- `rv_user_add_user_home_dir`
  - Type: `str`
  - Required: `false`
  - Description: Path to home

## Example Playbook

```yaml
- name: Add application user
  import_role:
    name: arpanrec.utilities.user_add
  vars:
    rv_user_add_username: "arpan"
    rv_user_add_ssh_access_public_key_content_list: ["ssh-rsa yc2E"]
```

## Testing

Prerequisite: `docker`, `python3-pip`

```bash
molecule test -s role.user_add.default
```

## License

`MIT`
